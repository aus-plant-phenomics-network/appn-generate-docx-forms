package tools.forms;

import org.docx4j.model.table.TblFactory;
import org.docx4j.openpackaging.exceptions.Docx4JException;
import org.docx4j.openpackaging.packages.WordprocessingMLPackage;
import org.docx4j.openpackaging.parts.WordprocessingML.HeaderPart;
import org.docx4j.openpackaging.parts.WordprocessingML.FooterPart;
import org.docx4j.openpackaging.parts.WordprocessingML.MainDocumentPart;
import org.docx4j.openpackaging.parts.WordprocessingML.BinaryPartAbstractImage;
import org.docx4j.openpackaging.parts.WordprocessingML.DocumentSettingsPart;
import org.docx4j.dml.wordprocessingDrawing.Inline;
import org.docx4j.relationships.Relationship;

// for embedding the YAML inside the word document
import org.docx4j.model.datastorage.CustomXmlDataStorageImpl;
import org.docx4j.openpackaging.parts.CustomXmlDataStoragePart;

/* import org.docx4j.wml.ObjectFactory;
import org.docx4j.wml.P;
import org.docx4j.wml.PPr;
import org.docx4j.wml.PPrBase;
import java.math.BigInteger; */

import org.docx4j.XmlUtils;
import org.w3c.dom.Document;

// for w14 checkbox JAXBElement fallback
import jakarta.xml.bind.JAXBElement;
import jakarta.xml.bind.JAXBException;
import jakarta.xml.bind.util.JAXBResult;
import javax.xml.namespace.QName;

import org.docx4j.wml.*;
import org.docx4j.w14.CTSdtCheckbox;
import org.docx4j.w14.CTSdtCheckboxSymbol;
import org.docx4j.w14.CTOnOff;

import org.docx4j.jaxb.Context;

import org.yaml.snakeyaml.Yaml;
import org.snakeyaml.engine.v2.api.Load;
import org.snakeyaml.engine.v2.api.LoadSettings;
import org.snakeyaml.engine.v2.api.ConstructNode;
import org.snakeyaml.engine.v2.nodes.Node;
import org.snakeyaml.engine.v2.nodes.MappingNode;

import java.io.File;                       // for pkg.save(new File(...))
import java.io.Reader;
import java.io.ByteArrayInputStream;       // for integrating YAML into Word XML
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.Path;
import java.math.BigInteger;
import java.awt.image.BufferedImage;
import javax.imageio.ImageIO;
import java.util.*;


public class GenerateDocxForm {

    // ------------ YAML model (keeps it simple & type-safe) -------------------
    public abstract static class Row {
        public String type; // "field" or "section"
        protected Row() {}
    }
    public static class Spec {
        private String title;
        private String formName;
        private String header_image;
        private String header_text;
        private String footer_text;
        private String section_count;  // use this to subtract te extra lines added by section
        private String note_start;  // add text at the start of the document
        private String note;
        private List<Row> rows = new ArrayList<>();

        public Spec() {
        }

        public String getTitle() {
            return title;
        }

        public void setTitle(String title) {
            this.title = title;
        }

        public String getFormName() {
            return formName;
        }

        public void setFormName(String formName) {
            this.formName = formName;
        }

        public String getHeader_image() {
            return header_image;
        }

        public void setHeader_image(String header_image) {
            this.header_image = header_image;
        }

        public String getHeader_text() {
            return header_text;
        }

        public void setHeader_text(String header_text) {
            this.header_text = header_text;
        }
        
        public String getFooter_text() {
            return footer_text;
        }
        
         public void setFooter_text(String footer_text) {
            this.footer_text = footer_text;
        }
        
        public String getSection_count() {
            return section_count;
        }
        
         public void setSection_count(String section_count) {
            this.section_count = section_count;
        }
        
        public String getNote_start() {
            return note_start;
        }

        public void setNote_start(String note) {
            this.note_start = note;
        }

        public String getNote() {
            return note;
        }

        public void setNote(String note) {
            this.note = note;
        }
        

        // THIS IS THE IMPORTANT PART
        public List<Row> getRows() {
            return rows;
        }

        public void setRows(List<Row> rows) {
            this.rows = rows;
        }
    }

    public static class Field extends Row {
        public String name;
        public String control;     // text | richtext | date | dropdown | combobox | checkbox | checkboxList
        public List<String> items;   // for dropdown/combobox/checkboxList
        public String label;  // was alias
        public String tag;
        public Boolean lockContentControl;
        public Boolean lockContents;
        
        public Field() {
            this.type = "field";
        }
        
    }
    
    public static class Section extends Row {
        public String text;
        public String background; 
        public Section() {
            this.type = "section";
        }
    }


    // ------------ Main -------------------------------------------------------
    public static void main(String[] args) throws Exception {
        Map<String, String> cli = parseArgs(args);
        String specPath = cli.get("--spec");
        String outPath  = cli.get("--out");
        if (specPath == null || outPath == null) {
            System.err.println("Usage: java -jar generate-docx-form.jar --spec <yaml> --out <docx>");
            System.exit(2);
        }
        
        LoadSettings settings = LoadSettings.builder().build();
        Load load = new Load(settings);

        Object data;
        try (InputStream in = Files.newInputStream(Paths.get(specPath))) {
            data = load.loadFromInputStream(in);
        }
        
        @SuppressWarnings("unchecked")
        Map<String, Object> root = (Map<String, Object>) data;

        Spec spec = new Spec();
        spec.setFormName((String) root.get("formName"));
        spec.setTitle((String) root.get("title"));
        spec.setHeader_image((String) root.get("header_image"));
        spec.setHeader_text((String) root.get("header_text"));
        spec.setFooter_text((String) root.get("footer_text"));
        spec.setSection_count((String) root.get("section_count"));
        spec.setNote_start((String) root.get("note_start"));
        spec.setNote((String) root.get("note"));
        
        
        @SuppressWarnings("unchecked")
        List<Map<String, Object>> rows =
                (List<Map<String, Object>>) root.get("rows");

        List<Row> result = new ArrayList<>();

        for (Map<String, Object> rowMap : rows) {

            String type = (String) rowMap.get("type");
            System.err.println(type);
             
            if ("field".equals(type)) {
                Field f = new Field();
                f.name = (String) rowMap.get("name");
                f.control = (String) rowMap.get("control");
                f.label = (String) rowMap.get("label");
                f.items = (List<String>) rowMap.get("items");
                result.add(f);

            } else if ("section".equals(type)) {
                Section s = new Section();
                s.text = (String) rowMap.get("text");
                s.background = (String) rowMap.get("background");
                result.add(s);

            } else {
                throw new IllegalArgumentException("Unknown row type: " + type);
            }
        }

        spec.setRows(result);

        if (spec == null) {
            throw new IllegalArgumentException("Empty or invalid YAML: " + specPath);
        }

        String yamlText = Files.readString(
                Paths.get(specPath), StandardCharsets.UTF_8);

        // Now use the model to create the docx form:
        buildForm(spec, outPath, yamlText);
        System.out.println("Created " + outPath);
    }

    private static Map<String, String> parseArgs(String[] args) {
        Map<String, String> out = new HashMap<>();
        for (int i=0; i<args.length-1; i++) {
            if (args[i].startsWith("--")) {
                out.put(args[i], args[i+1]);
                i++;
            }
        }
        return out;
    }

    // ------------ Document generation ---------------------------------------
    private static void buildForm(Spec spec, 
                                  String outPath,
                                  String yamlText
                                  ) throws Exception  {
        WordprocessingMLPackage pkg = WordprocessingMLPackage.createPackage(); // new blank docx
        
        // Add custom XML field containg YAML used to produce the docx file
        addYamlAsCustomXml(pkg, yamlText);
        
        addHeaderWithLogo(
            pkg,
            spec.header_image,
            spec.header_text
        );
        
        MainDocumentPart mdp = pkg.getMainDocumentPart();

        ObjectFactory f = new ObjectFactory();

        ensureWord2010Compatibility(pkg);
        
        // Title (centered); fallback to "<formName> Form" if title missing
        String title = (spec.title != null && !spec.title.isBlank())
                ? spec.title
                : ((spec.formName != null ? spec.formName.trim() : "") + " Form").trim();
        if (!title.isBlank()) {
            P p = f.createP();
            PPr ppr = f.createPPr();
            Jc jc = f.createJc();
            jc.setVal(JcEnumeration.CENTER);
            ppr.setJc(jc);
            p.setPPr(ppr);

            R r = f.createR();
            
            // Set title as bold
            RPr rpr = f.createRPr();
            BooleanDefaultTrue b = new BooleanDefaultTrue(); b.setVal(true);
            rpr.setB(b);
            r.setRPr(rpr);
            
            Text t = f.createText();
            t.setValue(title);
            r.getContent().add(t);
            p.getContent().add(r);
            mdp.addParagraphOfText(""); // blank line
            mdp.addObject(p);
            // mdp.addParagraphOfText(""); // blank line
        }
        
        // This is any text required before the table starts
        if (spec.note_start != null && !spec.note_start.isBlank()) {
            P pNote = para(f);
            R r = f.createR();

            String[] lines = spec.note_start.split("\\n");
            
            for (int i = 0; i < lines.length; i++) {
                Text t = f.createText();
                t.setValue(lines[i]);
                r.getContent().add(t);

                // Add line break except after last line
                if (i < lines.length - 1) {
                    r.getContent().add(f.createBr());
                }
            }
            
            pNote.getContent().add(r);
            mdp.addObject(pNote);
        }
        
        // counts number of sections to remove from the table
        // so it does not have extra lines
        int sub_extras = Integer.parseInt(spec.section_count); 
        if (spec.rows != null) {
            // For each row in the yaml 'rows' section
            for (int i=0; i<spec.rows.size(); i++) {
                Row row_yml = spec.rows.get(i);
                // Count if it is a 'section' block
                if (row_yml instanceof Section) 
                    sub_extras++;
            }
        }
        // Table with headers: "Field" | "Value"  - This has currently been left blank
        int writableWidthTwips = pkg.getDocumentModel()
                .getSections().get(0).getPageDimensions().getWritableWidthTwips();
        int cols = 2;
        int cellWidthTwips = (int)Math.floor((double)writableWidthTwips / cols);
        Tbl table = TblFactory.createTable(
                (spec.rows != null ? spec.rows.size()-sub_extras : 0) + 1, // header + rows
                cols,
                cellWidthTwips
        ); // TblFactory is a handy helper for basic tables in docx4j. [8](https://www.javatips.net/api/org.docx4j.model.table.tblfactory)

        // Header row
        // Tr header = (Tr) table.getContent().get(0);
        // setCellTextBold((Tc) header.getContent().get(0), "Detail", true);
        // setCellTextBold((Tc) header.getContent().get(1), "Value", true);

        // Rows
        if (spec.rows != null) {
            // For each row in the yaml 'rows' section
            for (int i=0; i<spec.rows.size(); i++) {
                Row row_yml = spec.rows.get(i);
                if (row_yml instanceof Section) {
                    Section section = (Section) row_yml;
                    
                    Tr sectionRow = createSectionRow(
                                    f,
                                    section,
                                    2   // number of table columns
                            );

                    table.getContent().add(i, sectionRow);

                } else if (row_yml instanceof Field) {

                    Field field = (Field) row_yml;
                    Tr row = (Tr) table.getContent().get(i);

                    // Column 1: label
                    String final_label =
                        !isBlank(field.label) ? field.label.trim() : field.name.trim();

                    setCellTextBold((Tc) row.getContent().get(0), nvl(final_label), true);

                    // Column 2: value cell DECLARED ONCE
                    Tc valueCell = (Tc) row.getContent().get(1);
                    valueCell.getContent().clear(); // important

                    if ("checkboxlist".equalsIgnoreCase(nvl(field.control))) {

                        if (field.items != null) {

                            for (String itemLabel : field.items) {
                                
                                // One paragraph per checkbox 
                                P itemPara = para(f);
                                
                                // Set the spacing between checkboxes so the hover-over 
                                // text does not block the one above
                                PPr pPr = f.createPPr();
                                PPrBase.Spacing spacing = f.createPPrBaseSpacing();
                                spacing.setAfter(BigInteger.valueOf(200)); // Twips (~10pt)
                                pPr.setSpacing(spacing);
                                itemPara.setPPr(pPr);

                                // Create per-item field
                                Field item = new Field();
                                item.control = "checkbox";

                                String baseAlias =
                                    !isBlank(field.name) ? field.name.trim() : "checkbox";

                                item.label = baseAlias + " [" + itemLabel + "]";
                                item.tag   = slugify(baseAlias + " " + itemLabel);

                                // Checkbox SDT
                                SdtRun sdt = makeSdtRunForField(f, item);
                                itemPara.getContent().add(sdt);

                                // Label text OUTSIDE the SDT 
                                itemPara.getContent().add(
                                    runWithText(f, " " + itemLabel)
                                );
                                
                                valueCell.getContent().add(itemPara);
                            }
                        }

                    } else {
                        // Single control (non-list)
                        P p = para(f);
                        SdtRun sdt = makeSdtRunForField(f, field);
                        p.getContent().add(sdt);
                        valueCell.getContent().add(p);
                    }
                }
            }
        }

        mdp.addObject(table);

        // Optional note (italic)
        if (spec.note != null && !spec.note.isBlank()) {
            mdp.addParagraphOfText(""); // space
            P pNote = para(f);
            R r = f.createR();
            RPr rpr = f.createRPr();
            BooleanDefaultTrue ital = new BooleanDefaultTrue(); ital.setVal(true);
            rpr.setI(ital);
            r.setRPr(rpr);
            
            
            // Text t = f.createText(); t.setValue(spec.note);
            // r.getContent().add(t);
            String[] lines = spec.note.split("\\n");

            for (int i = 0; i < lines.length; i++) {
                Text t = f.createText();
                t.setValue(lines[i]);
                r.getContent().add(t);

                // Add line break except after last line
                if (i < lines.length - 1) {
                    r.getContent().add(f.createBr());
                }
            }
            
            pNote.getContent().add(r);
            mdp.addObject(pNote);
        }
        
        
        addFooter(
            pkg,
            spec.footer_text
        );

        enableRestrictEditingForms(pkg);

        // Save
        pkg.save(new File(outPath));
    }




    public static boolean isParagraphVisiblyEmpty(P p) {
        if (p == null) return true;

        for (Object o : p.getContent()) {
            o = XmlUtils.unwrap(o);

            // SDTs (checkboxes, controls) count as visible
            if (o instanceof SdtBlock || o instanceof SdtRun) {
                return false;
            }

            if (o instanceof R) {
                R r = (R) o;

                for (Object ro : r.getContent()) {
                    ro = XmlUtils.unwrap(ro);

                    // Visible text
                    if (ro instanceof Text) {
                        String value = ((Text) ro).getValue();
                        if (value != null && !value.trim().isEmpty()) {
                            return false;
                        }
                    }

                    // Line breaks are visible
                    if (ro instanceof Br) {
                        return false;
                    }

                    // Images, drawings, fields, etc.
                    if (!(ro instanceof RPr)) {
                        return false;
                    }
                }
            }
        }

        return true;
    }


    public static void ensureWord2010Compatibility(WordprocessingMLPackage pkg)
    throws Exception {

        ObjectFactory factory = Context.getWmlObjectFactory();
        MainDocumentPart mdp = pkg.getMainDocumentPart();

        // Get or create settings part
        DocumentSettingsPart dsp = mdp.getDocumentSettingsPart();
        if (dsp == null) {
            dsp = new DocumentSettingsPart();
            CTSettings settings = factory.createCTSettings();
            dsp.setJaxbElement(settings);
            mdp.addTargetPart(dsp);
        }

        CTSettings settings = dsp.getJaxbElement();

        // Ensure <w:compat/> exists (prevents legacy mode)
        if (settings.getCompat() == null) {
            CTCompat compat = factory.createCTCompat();
            settings.setCompat(compat);
        }
    }

    // ------------ Helpers: cells, paragraphs, runs ---------------------------
    private static void setCellTextBold(Tc cell, String text, boolean bold) {
        // ObjectFactory f = Context.getWmlObjectFactory();
        ObjectFactory f = new ObjectFactory();
        P p = para(f);
        R r = f.createR();
        if (bold) {
            RPr rpr = f.createRPr();
            BooleanDefaultTrue b = new BooleanDefaultTrue(); b.setVal(true);
            rpr.setB(b);
            r.setRPr(rpr);
        }
        
        // Allow multi-line content in YAML using  ' label: |
        //                                             first line
        //                                             second line'
        // Text t = f.createText(); t.setValue(text);
        // r.getContent().add(t);
        String[] lines = text.split("\\n");

        for (int i = 0; i < lines.length; i++) {
            Text t = f.createText();
            t.setValue(lines[i]);
            r.getContent().add(t);

            // Add line break except after last line
            if (i < lines.length - 1) {
                r.getContent().add(f.createBr());
            }
        }
        

        p.getContent().add(r);
        setCellParagraph(cell, p);
    }

    private static void setCellParagraph(Tc cell, P p) {
        cell.getContent().clear();
        cell.getContent().add(p);
    }

    private static P para(ObjectFactory f) {
        return f.createP();
    }

    private static R runWithText(ObjectFactory f, String s) {
        R r = f.createR();
        Text t = f.createText(); 
        t.setValue(s);
        r.getContent().add(t);
        return r;
    }

    private static String nvl(String s) { return s == null ? "" : s; }

    // ------------ SDT creation (docx4j) -------------------------------------
    private static SdtRun makeSdtRunForField(ObjectFactory f, Field field) {
        String ctrl = (field.control == null ? "text" : field.control).toLowerCase(Locale.ROOT);

        SdtRun sdt = f.createSdtRun();
        SdtPr pr = f.createSdtPr();
        sdt.setSdtPr(pr);
        
        // ------ Label & Tag with slugify support ------
        // Human-friendly label: prefer YAML label, else YAML name, else YAML tag
        String aliasVal = coalesceNonBlank( field.name, field.tag);

        // Machine-friendly tag: prefer YAML tag, else slug(aliasVal)
        String tagVal = !isBlank(field.tag) ? field.tag.trim() : slugify(aliasVal);

        // If we still don't have anything, fall back to a generic slug from control type
        if (isBlank(aliasVal)) aliasVal = (isBlank(field.control) ? "field" : field.control.trim());
        if (isBlank(tagVal))   tagVal   = slugify(aliasVal);

        // Set BOTH Alias (Title) and Tag
        if (!isBlank(aliasVal)) {
            SdtPr.Alias aliasObj = new SdtPr.Alias();
            aliasObj.setVal(aliasVal);
            pr.getRPrOrAliasOrLock().add(f.createSdtPrAlias(aliasObj));
        }
        if (!isBlank(tagVal)) {
            Tag tagObj = f.createTag();
            tagObj.setVal(tagVal);
            pr.getRPrOrAliasOrLock().add(tagObj);
        }

        // Locking
        if (Boolean.TRUE.equals(field.lockContentControl)) {
            CTLock l = f.createCTLock();
            l.setVal(STLock.SDT_LOCKED);
            pr.getRPrOrAliasOrLock().add(f.createSdtPrLock(l));
        }
        if (Boolean.TRUE.equals(field.lockContents)) {
            CTLock l = f.createCTLock();
            l.setVal(STLock.CONTENT_LOCKED);
            pr.getRPrOrAliasOrLock().add(f.createSdtPrLock(l));
        }

        switch (ctrl) {
            case "dropdown": {
                CTSdtDropDownList dd = f.createCTSdtDropDownList();
                if (field.items != null) {
                    
                    if (field.items instanceof List) {

                        for (String value : (List<String>) field.items) {
                            if (value.contains("|")) {
                                String[] parts = value.split("\\|", 2);
                                addDropdownItem(parts[0], parts[1], dd);
                            } else {
                                addDropdownItem(value, value, dd);
                            }
                        }
                    }
                }
                pr.getRPrOrAliasOrLock().add(f.createSdtPrDropDownList(dd));
                break;
            }
            case "combobox": {
                CTSdtComboBox cb = f.createCTSdtComboBox();
                if (field.items != null) {
                    for (String it : field.items) {
                        CTSdtListItem li = new CTSdtListItem();
                        li.setDisplayText(String.valueOf(it));
                        li.setValue(String.valueOf(it));
                        cb.getListItem().add(li);
                    }
                }
                pr.getRPrOrAliasOrLock().add(f.createSdtPrComboBox(cb));
                break;
            }
           case "checkbox": {

                // --- w14 checkbox ---
                CTSdtCheckbox cb = new CTSdtCheckbox();

                // Default state: unchecked ("0"), checked = "1"
                CTOnOff checked = new CTOnOff();
                checked.setVal("0");
                cb.setChecked(checked);

                final String checkboxFont = "MS Gothic";

                // Checked symbol ☒ (U+2612)
                CTSdtCheckboxSymbol checkedSym = new CTSdtCheckboxSymbol();
                checkedSym.setVal("2612");
                checkedSym.setFont(checkboxFont);
                cb.setCheckedState(checkedSym);

                // Unchecked symbol ☐ (U+2610)
                CTSdtCheckboxSymbol uncheckedSym = new CTSdtCheckboxSymbol();
                uncheckedSym.setVal("2610");
                uncheckedSym.setFont(checkboxFont);
                cb.setUncheckedState(uncheckedSym);

                // Attach checkbox to SDT properties (no factory helper exists)
                QName qn = new QName(
                    "http://schemas.microsoft.com/office/word/2010/wordml",
                    "checkbox"
                );

                JAXBElement<CTSdtCheckbox> checkboxEl =
                    new JAXBElement<>(qn, CTSdtCheckbox.class, cb);

                pr.getRPrOrAliasOrLock().add(checkboxEl);
                
                break;
            }
            case "date": {
                CTSdtDate date = f.createCTSdtDate();

                // Format: yyyy-MM-dd  (you can change this to another format)
                CTSdtDate.DateFormat df = new CTSdtDate.DateFormat();
                df.setVal("yyyy-MM-dd");
                date.setDateFormat(df);

                // Optional <w:lid> language ID is not required; omit it to avoid class-mismatch issues

                pr.getRPrOrAliasOrLock().add(f.createSdtPrDate(date));
                break;
            }
            case "richtext": {
                // Rich text control marker lives in CTSdtRichText? In practice, an empty run content under SDT is fine.
                // If you need explicit marker, plain text SDT also works for free text entry.
                // We'll leave it as a generic SDT and rely on content area.
                break;
            }
            case "text":
            default: {
                CTSdtText tx = f.createCTSdtText();
                pr.getRPrOrAliasOrLock().add(f.createSdtPrText(tx));
                break;
            }
        }

        // Content container (inline SDT)
        CTSdtContentRun content = f.createCTSdtContentRun();

        // If it’s a checkbox, seed with the appropriate glyph so it shows up right away
        if ("checkbox".equals(ctrl)) {
            // If you set a checked default above, pass true here.
            appendCheckboxGlyphRun(f, content, /*checked=*/false, "MS Gothic"); // or "Segoe UI Symbol"
        } else {
            content.getContent().add(runWithText(f, "")); // default empty
        }

        sdt.setSdtContent(content);
        return sdt;

    }

    private static void addDropdownItem(String displayText,
                                        String value,
                                        CTSdtDropDownList dd) {
        CTSdtListItem li = new CTSdtListItem();
        li.setDisplayText(displayText);
        li.setValue(value);
        dd.getListItem().add(li);    
    }
    
    /**
     * Appends a run to the given CTSdtContentRun with a checkbox glyph,
     * using a symbol-capable font so it renders reliably in Word.
     *
     * @param f        WML ObjectFactory
     * @param content  The inline SDT content container to append to
     * @param checked  true = ☒ (U+2612), false = ☐ (U+2610)
     * @param font     A font that contains the glyphs, e.g. "MS Gothic" or "Segoe UI Symbol"
     */
    private static void appendCheckboxGlyphRun(ObjectFactory f,
                                               CTSdtContentRun content,
                                               boolean checked,
                                               String font) {
        final String glyph = checked ? "\u2612" : "\u2610"; // ☒ or ☐

        // Build a run with font hints so Word picks the right glyph
        R r = f.createR();
        RPr rpr = f.createRPr();
        RFonts rFonts = f.createRFonts();
        rFonts.setAscii(font);
        rFonts.setHAnsi(font);
        rFonts.setEastAsia(font);
        rFonts.setCs(font);
        rpr.setRFonts(rFonts);
        r.setRPr(rpr);

        Text t = f.createText();
        t.setValue(glyph);
        r.getContent().add(t);

        content.getContent().add(r);
    }


    /** Returns true if the string is null/blank */
    private static boolean isBlank(String s) {
        return s == null || s.trim().isEmpty();
    }

    /**
     * Slugify a string for use as a programmatic tag.
     * - Trim
     * - Lowercase
     * - Replace any non [a-z0-9]+ with single hyphen
     * - Collapse multiple hyphens
     * - Strip leading/trailing hyphens
     * If the input is null/blank, returns null.
     */
    private static String slugify(String input) {
        if (isBlank(input)) return null;
        String s = input.trim().toLowerCase(Locale.ROOT);
        // Replace all non-alphanumeric with hyphen
        s = s.replaceAll("[^a-z0-9]+", "-");
        // Collapse multiple hyphens
        s = s.replaceAll("-{2,}", "-");
        // Trim leading/trailing hyphens
        s = s.replaceAll("^-|-$", "");
        return s;
    }

    /** Returns the first non-blank value */
    private static String coalesceNonBlank(String... items) {
        if (items == null) return null;
        for (String s : items) {
            if (!isBlank(s)) return s.trim();
        }
        return null;
    }
    
    public static void addHeaderWithLogo(
        WordprocessingMLPackage wordMLPackage,
        String imagePath,
        String headerText
    ) throws Exception {

        ObjectFactory factory = Context.getWmlObjectFactory();

        // Create header part
        HeaderPart headerPart = new HeaderPart();
        headerPart.setPackage(wordMLPackage);

        Hdr  header = factory.createHdr();
        headerPart.setJaxbElement(header);

        // Add header relationship
        Relationship rel = wordMLPackage
                .getMainDocumentPart()
                .addTargetPart(headerPart);

        // Create table for layout (2 columns: logo | text)
        Tbl table = createHeaderTable(factory, wordMLPackage, headerPart, imagePath, headerText);

        header.getContent().add(table);

        // Attach header to section
        SectPr sectPr = getOrCreateSectPr(wordMLPackage);
        HeaderReference headerRef = factory.createHeaderReference();
        headerRef.setId(rel.getId());
        headerRef.setType(HdrFtrRef.DEFAULT);
        sectPr.getEGHdrFtrReferences().add(headerRef);
    }


    private static Tbl createHeaderTable(
            ObjectFactory factory,
            WordprocessingMLPackage wordMLPackage,
            HeaderPart headerPart,
            String imagePath,
            String headerText
    ) throws Exception {

        Tbl table = factory.createTbl();

        // Table properties
        TblPr tblPr = factory.createTblPr();
        TblWidth width = factory.createTblWidth();
        width.setType("pct");
        width.setW(BigInteger.valueOf(5000)); // 100%
        tblPr.setTblW(width);
        table.setTblPr(tblPr);

        Tr row = factory.createTr();

        Path logoPath = Paths.get(imagePath);
        if (Files.exists(logoPath)) {
            // Logo cell
            Tc logoCell = factory.createTc();

            P logoPara = createHeaderImageParagraph(
                    wordMLPackage,
                    headerPart,
                    factory,
                    imagePath,
                    1.5   // height in cm
            );
            logoCell.getContent().add(logoPara);
            row.getContent().add(logoCell);
        } else {
           System.out.println("INFO: Could not find logo image for header: " + imagePath);
        }
        
        // Text cell
        Tc textCell = factory.createTc();
        P textPara= createTextParagraph(factory, headerText);
        textCell.getContent().add(textPara);
        row.getContent().add(textCell);
        
        
        table.getContent().add(row);
        
        addBottomBorder(table);

        return table;
    }
    
    
    private static void addBottomBorder(Tbl table) {

        ObjectFactory factory = Context.getWmlObjectFactory();

        TblPr tblPr = table.getTblPr();
        if (tblPr == null) {
            tblPr = factory.createTblPr();
            table.setTblPr(tblPr);
        }

        TblBorders borders = factory.createTblBorders();

        CTBorder bottom = factory.createCTBorder();
        bottom.setVal(STBorder.SINGLE);
        bottom.setSz(BigInteger.valueOf(8)); // 0.5pt
        bottom.setSpace(BigInteger.ZERO);
        bottom.setColor("auto");

        borders.setBottom(bottom);
        tblPr.setTblBorders(borders);
    }

    
    private static final long EMU_PER_CM = 360000L;
    private static final long EMU_PER_PX = 9525L;
    
    private static P createHeaderImageParagraph(
            WordprocessingMLPackage pkg,
            HeaderPart headerPart,
            ObjectFactory factory,
            String imagePath,
            double targetHeightCm
    ) throws Exception {

        // --- constants (OOXML standard) ---
        final long EMU_PER_CM = 360000L;
        final long EMU_PER_PX = 9525L; // assumes 96 DPI

        // --- load image ---
        File imageFile = new File(imagePath);
        if (!imageFile.exists()) {
            throw new IllegalArgumentException("Image not found: " + imagePath);
        }

        BufferedImage img = ImageIO.read(imageFile);
        if (img == null) {
            throw new IllegalStateException("ImageIO could not read image: " + imagePath);
        }

        int pxWidth = img.getWidth();
        int pxHeight = img.getHeight();

        // --- calculate size (preserve aspect ratio) ---
        long heightEmu = Math.round(targetHeightCm * EMU_PER_CM);
        long widthEmu = Math.round(((double) pxWidth / pxHeight) * heightEmu);

        // --- read bytes ---
        byte[] bytes = Files.readAllBytes(imageFile.toPath());

        // ✅ IMPORTANT: create the image part ON THE HEADER PART
        BinaryPartAbstractImage imagePart =
                BinaryPartAbstractImage.createImagePart(pkg, headerPart, bytes);

        Inline inline = imagePart.createImageInline(
                "Header Logo",   // alt text
                "Header Logo",   // description
                1,               // id (any unique int)
                2,               // docPrId (any unique int)
                widthEmu,
                heightEmu,
                false            // no hyperlink
        );

        // --- wrap in Drawing / Run / Paragraph ---
        Drawing drawing = factory.createDrawing();
        drawing.getAnchorOrInline().add(inline);

        R run = factory.createR();
        run.getContent().add(drawing);

        P paragraph = factory.createP();
        paragraph.getContent().add(run);

        return paragraph;
    }
    
    private static P createTextParagraph(ObjectFactory factory, String headerText) {
        P titlePara = factory.createP();
        R run = factory.createR();

        Text text = factory.createText();
        text.setValue(headerText);
        run.getContent().add(text);

        // optional styling
        RPr rPr = factory.createRPr();
        BooleanDefaultTrue bold = new BooleanDefaultTrue();
        rPr.setB(bold);

        HpsMeasure size = new HpsMeasure();
        size.setVal(BigInteger.valueOf(28)); // 14pt
        rPr.setSz(size);
        rPr.setSzCs(size);

        run.setRPr(rPr);
        titlePara.getContent().add(run);

        return titlePara;
    }

    private static SectPr getOrCreateSectPr(WordprocessingMLPackage wordMLPackage) {
        Body body = wordMLPackage.getMainDocumentPart().getJaxbElement().getBody();
        SectPr sectPr = body.getSectPr();
        if (sectPr == null) {
            sectPr = Context.getWmlObjectFactory().createSectPr();
            body.setSectPr(sectPr);
        }
        return sectPr;
    }
    
    private static Tr createSectionRow(
            ObjectFactory factory,
            Section section,
            int totalColumns
    ) {

        Tr row = factory.createTr();
        Tc cell = factory.createTc();

        // --- span across all columns ---
        TcPr tcPr = factory.createTcPr();
        TcPrInner.GridSpan gridSpan = factory.createTcPrInnerGridSpan();
        gridSpan.setVal(BigInteger.valueOf(totalColumns));
        tcPr.setGridSpan(gridSpan);

        // --- apply background shading ---
        CTShd shd = factory.createCTShd();
        shd.setVal(STShd.CLEAR);
        shd.setColor("auto");
        shd.setFill(resolveColour(section.background));

        tcPr.setShd(shd);
        cell.setTcPr(tcPr);

        // --- section text ---
        P p = factory.createP();
        R r = factory.createR();


        String[] lines = section.text.split("\\n");

        for (int i = 0; i < lines.length; i++) {
            Text t = factory.createText();
            t.setValue(lines[i]);
            r.getContent().add(t);

            // Add line break except after last line
            if (i < lines.length - 1) {
                r.getContent().add(factory.createBr());
            }
        }

        // --- run properties (bold + white text) ---
        RPr rPr = factory.createRPr();

        // bold
        rPr.setB(new BooleanDefaultTrue());

        // ✅ text colour = white
        Color color = factory.createColor();
        color.setVal("FFFFFF");
        rPr.setColor(color);

        r.setRPr(rPr);

        p.getContent().add(r);
        cell.getContent().add(p);

        row.getContent().add(cell);
        return row;
    }
    
    private static String resolveColour(String colour) {
        if (colour == null || colour.isBlank()) {
            return "F2F2F2"; // default light grey
        }

        // hex value provided
        if (colour.startsWith("#")) {
            return colour.substring(1);
        }

        // named colours (extend as needed)
        switch (colour.toLowerCase()) {
            case "light green":
                return "D9EAD3";
            case "light blue":
                return "D9E1F2";
            case "light yellow":
                return "FFF2CC";
            case "light grey":
            case "light gray":
                return "F2F2F2";
            default:
                return "F2F2F2";
        }
    }
    
    public static void addFooter(
            WordprocessingMLPackage wordMLPackage,
            String infoText
    ) throws Exception {

        ObjectFactory factory = Context.getWmlObjectFactory();

        // Create footer part
        FooterPart footerPart = new FooterPart();
        footerPart.setPackage(wordMLPackage);

        Ftr footer = factory.createFtr();
        footerPart.setJaxbElement(footer);

        // Add footer relationship
        Relationship rel = wordMLPackage
                .getMainDocumentPart()
                .addTargetPart(footerPart);

        // Create footer table
        Tbl footerTable = createFooterTable(factory, infoText);
        footer.getContent().add(footerTable);

        // Attach footer to section
        SectPr sectPr = getOrCreateSectPr(wordMLPackage);
        FooterReference footerRef = factory.createFooterReference();
        footerRef.setId(rel.getId());
        footerRef.setType(HdrFtrRef.DEFAULT);
        sectPr.getEGHdrFtrReferences().add(footerRef);
    }
    
    private static Tbl createFooterTable(
            ObjectFactory factory,
            String infoText
    ) {

        Tbl table = factory.createTbl();

        // Table width = 100%
        TblPr tblPr = factory.createTblPr();
        TblWidth width = factory.createTblWidth();
        width.setType("pct");
        width.setW(BigInteger.valueOf(5000));
        tblPr.setTblW(width);
        table.setTblPr(tblPr);

        Tr row = factory.createTr();

        // Left: Info text
        row.getContent().add(createCell(factory,
                createTextParagraph(factory, infoText, JcEnumeration.LEFT)));

        // Center: Date field
        row.getContent().add(createCell(factory,
                createDateFieldParagraph(factory)));

        // Right: Page X of Y
        row.getContent().add(createCell(factory,
                createPageXofYParagraph(factory)));

        table.getContent().add(row);
        return table;
    }
    
    private static Tc createCell(ObjectFactory factory, P paragraph) {
        Tc cell = factory.createTc();
        cell.getContent().add(paragraph);
        return cell;
    }
    
    private static P createTextParagraph(
            ObjectFactory factory,
            String text,
            JcEnumeration alignment
    ) {

        P p = factory.createP();
        PPr pPr = factory.createPPr();
        Jc jc = factory.createJc();
        jc.setVal(alignment);
        pPr.setJc(jc);
        p.setPPr(pPr);

        R r = factory.createR();
        Text t = factory.createText();
        t.setValue(text);
        r.getContent().add(t);
        
        applySmallFooterFont(factory, r);
        p.getContent().add(r);

        return p;
    }
    
    private static P createDateFieldParagraph(ObjectFactory factory) {

        P p = factory.createP();
        setParagraphAlignment(factory, p, JcEnumeration.CENTER);

        R begin = createFldChar(factory, STFldCharType.BEGIN);
        applySmallFooterFont(factory, begin);
        p.getContent().add(begin);

        R instr = createInstrText(factory, " DATE \\@ \"dd MMM yyyy\" ");
        applySmallFooterFont(factory, instr);
        p.getContent().add(instr);

        R end = createFldChar(factory, STFldCharType.END);
        applySmallFooterFont(factory, end);
        p.getContent().add(end);

        return p;
    }
    
    private static P createPageXofYParagraph(ObjectFactory factory) {

        P p = factory.createP();
        setParagraphAlignment(factory, p, JcEnumeration.RIGHT);

        // "Page "
        R pageText = factory.createR();
        Text pageLabel = factory.createText();
        pageLabel.setValue("Page ");
        pageLabel.setSpace("preserve");
        pageText.getContent().add(pageLabel);
        applySmallFooterFont(factory, pageText);
        p.getContent().add(pageText);

        // PAGE field
        R pageBegin = createFldChar(factory, STFldCharType.BEGIN);
        applySmallFooterFont(factory, pageBegin);
        p.getContent().add(pageBegin);

        R pageInstr = createInstrText(factory, " PAGE ");
        applySmallFooterFont(factory, pageInstr);
        p.getContent().add(pageInstr);

        R pageEnd = createFldChar(factory, STFldCharType.END);
        applySmallFooterFont(factory, pageEnd);
        p.getContent().add(pageEnd);

        // " of "
        R ofText = factory.createR();
        Text ofLabel = factory.createText();
        ofLabel.setValue(" of ");
        ofLabel.setSpace("preserve");
        ofText.getContent().add(ofLabel);
        applySmallFooterFont(factory, ofText);
        p.getContent().add(ofText);

        // NUMPAGES field
        R numBegin = createFldChar(factory, STFldCharType.BEGIN);
        applySmallFooterFont(factory, numBegin);
        p.getContent().add(numBegin);

        R numInstr = createInstrText(factory, " NUMPAGES ");
        applySmallFooterFont(factory, numInstr);
        p.getContent().add(numInstr);

        R numEnd = createFldChar(factory, STFldCharType.END);
        applySmallFooterFont(factory, numEnd);
        p.getContent().add(numEnd);

        return p;
    }
    
    private static R createFldChar(ObjectFactory factory, STFldCharType type) {
        R r = factory.createR();
        FldChar fldChar = factory.createFldChar();
        fldChar.setFldCharType(type);
        r.getContent().add(fldChar);
        return r;
    }

    private static R createInstrText(ObjectFactory factory, String text) {
        R r = factory.createR();
        Text t = factory.createText();
        t.setValue(text);
        t.setSpace("preserve");
        r.getContent().add(t);
        return r;
    }
    
    private static void setParagraphAlignment(
            ObjectFactory factory,
            P p,
            JcEnumeration align
    ) {
        PPr pPr = p.getPPr();
        if (pPr == null) {
            pPr = factory.createPPr();
            p.setPPr(pPr);
        }
        Jc jc = factory.createJc();
        jc.setVal(align);
        pPr.setJc(jc);
    }
    
    private static void applySmallFooterFont(ObjectFactory factory, R run) {

        RPr rPr = run.getRPr();
        if (rPr == null) {
            rPr = factory.createRPr();
            run.setRPr(rPr);
        }

        // 9pt font (18 half-points)
        HpsMeasure fontSize = factory.createHpsMeasure();
        fontSize.setVal(BigInteger.valueOf(18));
        rPr.setSz(fontSize);
        rPr.setSzCs(fontSize);
    }
    
    public static void enableRestrictEditingForms(WordprocessingMLPackage pkg) 
    throws Exception {

        ObjectFactory factory = Context.getWmlObjectFactory();
        MainDocumentPart mdp = pkg.getMainDocumentPart();

        // Get or create settings part
        DocumentSettingsPart dsp = mdp.getDocumentSettingsPart();
        if (dsp == null) {
            dsp = new DocumentSettingsPart();
            dsp.setJaxbElement(factory.createCTSettings());
            mdp.addTargetPart(dsp);
        }

        CTSettings settings = dsp.getJaxbElement();

        // Create document protection
        CTDocProtect protect = factory.createCTDocProtect();
        protect.setEdit(STDocProtect.FORMS);     // ✅ Filling in forms
        protect.setEnforcement(Boolean.TRUE);    // ✅ Enable protection

        // Optional but recommended
        protect.setFormatting(Boolean.FALSE);
        //protect.setComments(Boolean.FALSE);
        //protect.setTrackRevisions(Boolean.FALSE);

        settings.setDocumentProtection(protect);
    }
    


    
    public static SdtRun createCheckboxSdtRun(
            ObjectFactory factory,
            boolean checked
    ) {
        // SDT container
        SdtRun sdt = factory.createSdtRun();

        // SDT properties
        SdtPr pr = factory.createSdtPr();

        // --- w14 checkbox ---
        CTSdtCheckbox cb = new CTSdtCheckbox();

        CTOnOff onOff = new CTOnOff();
        onOff.setVal(checked ? "1" : "0"); // "1"=checked, "0"=unchecked
        cb.setChecked(onOff);

        final String checkboxFont = "MS Gothic";

        CTSdtCheckboxSymbol checkedSym = new CTSdtCheckboxSymbol();
        checkedSym.setVal("2612"); // ☒
        checkedSym.setFont(checkboxFont);

        CTSdtCheckboxSymbol uncheckedSym = new CTSdtCheckboxSymbol();
        uncheckedSym.setVal("2610"); // ☐
        uncheckedSym.setFont(checkboxFont);

        cb.setCheckedState(checkedSym);
        cb.setUncheckedState(uncheckedSym);

        QName qn = new QName(
            "http://schemas.microsoft.com/office/word/2010/wordml",
            "checkbox"
        );

        JAXBElement<CTSdtCheckbox> el =
            new JAXBElement<>(qn, CTSdtCheckbox.class, cb);

        pr.getRPrOrAliasOrLock().add(el);
        sdt.setSdtPr(pr);

        // ✅ docx4j 11.x: content is accessed, not created
        sdt.getSdtContent().getContent().add(factory.createR());

        return sdt;
    }
    


    private static void addYamlAsCustomXml(
            WordprocessingMLPackage pkg,
            String yamlText
    ) throws Exception {

        String xml =
            "<appn:docxFormSpec xmlns:appn=\"https://schema.plantphenomics.org.au/docx-form\">\n" +
            "  <![CDATA[\n" +
            yamlText +
            "\n  ]]>\n" +
            "</appn:docxFormSpec>";

        CustomXmlDataStoragePart customPart = new CustomXmlDataStoragePart();

        // ✅ REQUIRED in docx4j 11
        CustomXmlDataStorageImpl data = new CustomXmlDataStorageImpl();
        data.setDocument(
            new ByteArrayInputStream(xml.getBytes(StandardCharsets.UTF_8))
        );
        customPart.setData(data);

        pkg.getMainDocumentPart().addTargetPart(customPart);
    }
    
    


}