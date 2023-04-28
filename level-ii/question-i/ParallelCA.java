import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;
import java.util.List;

public class ParallelCA extends CellularAutomata {
  public ParallelCA(String filepath) {
    super(filepath);
  }

  @Override
  public List<List<Integer>> computeNextGeneration() {
    List<List<Integer>> nextGenerationMatrix = new ArrayList<>(getRowCount());
    ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
    for (int i = 0; i < getRowCount(); i++) {
      final int rowIndex = i;
      executor.execute(() -> {
        List<Integer> row = new ArrayList<>(getColumnCount());
        for (int j = 0; j < getColumnCount(); j++) {
          int cell = getMatrix().get(rowIndex).get(j);
          int neighbors = getCellNeighbors(rowIndex, j);

          if (cell == 0 && (neighbors > 1 && neighbors < 5)) {
            row.add(1);
          } else if (cell == 1) {
            if (neighbors > 3 && neighbors < 6) {
              row.add(1);
            } else {
              row.add(0);
            }
          } else {
            row.add(cell);
          }
        }
        synchronized (nextGenerationMatrix) {
          nextGenerationMatrix.add(row);
        }
      });
    }
    executor.shutdown();
    try {
      executor.awaitTermination(Long.MAX_VALUE, TimeUnit.NANOSECONDS);
    } catch (InterruptedException e) {
      e.printStackTrace();
    }
    return nextGenerationMatrix;
  }
}
