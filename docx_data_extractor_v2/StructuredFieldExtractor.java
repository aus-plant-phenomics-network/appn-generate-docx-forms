import org.apache.poi.xwpf.usermodel.*;

import java.io.FileInputStream;
import java.util.ArrayList;
import java.util.List;

public class StructuredFieldExtractor {

    public record Field(
            String name,
            String value,
            int tableIndex,
            int rowIndex,
            int columnIndex
    ) {}

    public static void main(String[] args) throws Exception {

        if (args.length != 1) {
            System.err.println("Usage: java StructuredFieldExtractor <docx-file>");
            System.exit(1);
        }

        try (FileInputStream fis = new FileInputStream(args[0]);
             XWPFDocument document = new XWPFDocument(fis)) {

            List<Field> fields = extractFields(document);

            for (Field field : fields) {
                System.out.printf(
                        "Field[name='%s', value='%s', table=%d, row=%d, col=%d]%n",
                        field.name(),
                        field.value(),
                        field.tableIndex(),
                        field.rowIndex(),
                        field.columnIndex());
            }
        }
    }

    private static List<Field> extractFields(XWPFDocument document) {

        List<Field> fields = new ArrayList<>();

        List<XWPFTable> tables = document.getTables();

        for (int tableIndex = 0; tableIndex < tables.size(); tableIndex++) {

            XWPFTable table = tables.get(tableIndex);

            for (int rowIndex = 0; rowIndex < table.getRows().size(); rowIndex++) {

                XWPFTableRow row = table.getRows().get(rowIndex);

                List<XWPFTableCell> cells = row.getTableCells();

                for (int colIndex = 0; colIndex < cells.size() - 1; colIndex++) {

                    String label = clean(cells.get(colIndex).getText());
                    String value = clean(cells.get(colIndex + 1).getText());

                    if (looksLikeLabel(label)) {
                        fields.add(new Field(label, value, tableIndex, rowIndex, colIndex));
                    }
                }
            }
        }

        return fields;
    }

    private static boolean looksLikeLabel(String text) {
        if (text == null || text.isBlank()) {
            return false;
        }

        return text.endsWith(":")
                || text.contains("Name")
                || text.contains("Email")
                || text.contains("Phone")
                || text.contains("Mobile")
                || text.contains("Address")
                || text.contains("Organisation")
                || text.contains("Department")
                || text.contains("Description")
                || text.contains("Project");
    }

    private static String clean(String text) {
        return text == null ? "" : text.replaceAll("\\s+", " ").trim();
    }
}
