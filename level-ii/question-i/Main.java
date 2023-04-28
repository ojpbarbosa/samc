public class Main {
  public static void main(String[] args) {
    CellularAutomata cellularAutomata = new ParallelBitFlipper("ffff.txt");

    long totalStart = System.currentTimeMillis();
    for (int i = 0; i < 100; i++) {
      long generationStart = System.currentTimeMillis();
      cellularAutomata.attributeNextGeneration();
      long generationEnd = System.currentTimeMillis();
      double generationTime = (generationEnd - generationStart) / 1000.0;
      System.out.printf("Generation %d time: %f\n", i, generationTime);
    }
    long totalEnd = System.currentTimeMillis();
    double totalTime = (totalEnd - totalStart) / 1000.0;
    System.out.printf("Total time: %f\n", totalTime);
  }
}
