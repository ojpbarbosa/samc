import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class CellularAutomata {
  private String filepath;
  private List<List<Integer>> matrix;
  private int rowCount;
  private int columnCount;

  public String getFilepath() {
    return filepath;
  }

  public List<List<Integer>> getMatrix() {
    return matrix;
  }

  public int getRowCount() {
    return rowCount;
  }

  public int getColumnCount() {
    return columnCount;
  }

  public CellularAutomata(String filepath) {
    this.filepath = filepath;
    loadMatrix();
  }

  public void attributeNextGeneration() {
    matrix = computeNextGeneration();
  }

  public List<List<Integer>> computeNextGeneration() {
    List<List<Integer>> nextGenerationMatrix = new ArrayList<>(rowCount);
    for (int i = 0; i < rowCount; i++) {
      nextGenerationMatrix.add(new ArrayList<>(columnCount));
      for (int j = 0; j < columnCount; j++) {
        int cell = matrix.get(i).get(j);
        int neighbors = getCellNeighbors(i, j);

        if (cell == 0 && (neighbors > 1 && neighbors < 5)) {
          nextGenerationMatrix.get(i).add(1);
        } else if (cell == 1) {
          if (neighbors > 3 && neighbors < 6) {
            nextGenerationMatrix.get(i).add(1);
          } else {
            nextGenerationMatrix.get(i).add(0);
          }
        } else {
          nextGenerationMatrix.get(i).add(cell);
        }
      }
    }
    return nextGenerationMatrix;
  }

  public int getCellNeighbors(int i, int j) {
    int neighbors = 0;
    for (int x = -1; x < 2; x++) {
      for (int y = -1; y < 2; y++) {
        if (x == 0 && y == 0) {
          continue;
        }

        int iEdge = i + x;
        int jEdge = j + y;

        if (iEdge < 0 || iEdge >= rowCount || jEdge < 0 || jEdge >= columnCount) {
          continue;
        }

        int edgeCell = matrix.get(iEdge).get(jEdge);
        if (edgeCell == 1) {
          neighbors++;
        }
      }
    }
    return neighbors;
  }

  public void loadMatrix() {
    try (BufferedReader br = new BufferedReader(new FileReader(filepath))) {
      List<List<Integer>> rows = new ArrayList<>();
      String line;
      while ((line = br.readLine()) != null) {
        List<Integer> row = new ArrayList<>();
        for (char character : line.toCharArray()) {
          row.add(Character.getNumericValue(character));
        }
        rows.add(row);
      }
      rowCount = rows.size();
      columnCount = rows.get(0).size();
      matrix = new ArrayList<>(rowCount);
      for (int i = 0; i < rowCount; i++) {
        matrix.add(new ArrayList<>(columnCount));
        for (int j = 0; j < columnCount; j++) {
          matrix.get(i).add(rows.get(i).get(j));
        }
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
