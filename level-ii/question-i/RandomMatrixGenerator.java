import java.io.File;
import java.io.FileWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

public class RandomMatrixGenerator {

  public static void main(String[] args) {
    // Set dimensions of the matrix
    int rows = 56420;
    int cols = 56420;

    // Set probability of generating 1s
    double prob = 0.5;

    // Set number of threads to use
    int numThreads = Runtime.getRuntime().availableProcessors();

    // Create a Random object
    Random rand = new Random();

    // Create a StringBuilder object to store the matrix
    StringBuilder matrix = new StringBuilder();

    // Create a list of Callables to generate the rows of the matrix
    List<Callable<String>> rowGenerators = new ArrayList<>();
    for (int i = 0; i < rows; i++) {
      final int row = i;
      rowGenerators.add(() -> generateRow(row, cols, prob, rand));
    }

    // Create an ExecutorService with the specified number of threads
    ExecutorService executorService = Executors.newFixedThreadPool(numThreads);

    try {
      // Invoke all Callables and store the Future objects
      List<Future<String>> futures = executorService.invokeAll(rowGenerators);

      // Append each row to the StringBuilder
      for (Future<String> future : futures) {
        matrix.append(future.get());
      }

      // Write the matrix to a file
      File file = new File("random_matrix.txt");
      FileWriter writer = new FileWriter(file);
      writer.write(matrix.toString());
      writer.close();
      System.out.println("Matrix generated and written to " + file.getAbsolutePath());

    } catch (Exception e) {
      System.out.println("An error occurred while generating the matrix.");
      e.printStackTrace();
    } finally {
      // Shutdown the ExecutorService
      executorService.shutdown();
    }
  }

  private static String generateRow(int row, int cols, double prob, Random rand) {
    StringBuilder rowBuilder = new StringBuilder();
    for (int j = 0; j < cols; j++) {
      if (rand.nextDouble() < prob) {
        rowBuilder.append("1 ");
      } else {
        rowBuilder.append("0 ");
      }
    }
    rowBuilder.append("\n");
    return rowBuilder.toString();
  }
}
