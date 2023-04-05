#include <fstream>
#include <vector>
#include <cmath>
#include <iostream>
#include <chrono>
#include <ctime>
// #include <omp.h>

using namespace std;

class CellularAutomata
{
public:
  CellularAutomata(const std::string filepath) : filepath(filepath)
  {
    generation = 0;
    load_matrix();
  }

  void attribute_next_generation()
  {
    matrix = compute_next_generation();
    generation++;
  }

  std::vector<std::vector<int> > compute_next_generation()
  {
    std::vector<std::vector<int> > next_generation_matrix(row_count, std::vector<int>(column_count));

// #pragma omp parallel for
    for (int i = 0; i < row_count; i++)
    {
      for (int j = 0; j < column_count; j++)
      {
        int cell = matrix[i][j];

        int neighbors = get_cell_neighbors(i, j);

        if (cell == 0 && (neighbors > 1 && neighbors < 5))
        {
          next_generation_matrix[i][j] = 1;
        }

        else if (cell == 1)
        {
          if (neighbors > 3 && neighbors < 6)
          {
            next_generation_matrix[i][j] = 1;
          }
          else
          {
            next_generation_matrix[i][j] = 0;
          }
        }

        else
        {
          next_generation_matrix[i][j] = cell;
        }
      }
    }

    return next_generation_matrix;
  }

  int get_cell_neighbors(int i, int j)
  {
    int neighbors = 0;

    for (int x = -1; x < 2; x++)
    {
      for (int y = -1; y < 2; y++)
      {
        if (x == 0 && y == 0)
        {
          continue;
        }

        int i_edge = i + x;
        int j_edge = j + y;

        if (i_edge < 0 || i_edge >= row_count || j_edge < 0 || j_edge >= column_count)
        {
          continue;
        }

        int edge_cell = matrix[i_edge][j_edge];

        if (edge_cell == 1)
        {
          neighbors++;
        }
      }
    }

    return neighbors;
  }

  void load_matrix()
  {
    std::ifstream file(filepath);
    std::vector<std::vector<int> > rows;

    std::string line;
    while (std::getline(file, line))
    {
      std::vector<int> row;
      for (char character : line)
      {
        if (isspace(character))
        {
          continue;
        }

        row.push_back((int)character - '0');
      }

      rows.push_back(row);
    }

    row_count = rows.size();
    column_count = rows[0].size();
    matrix.resize(row_count, std::vector<int>(column_count));

    for (int i = 0; i < row_count; i++)
    {
      for (int j = 0; j < column_count; j++)
      {
        matrix[i][j] = rows[i][j];
      }
    }
  }

private:
  std::string filepath;
  std::vector<std::vector<int> > matrix;
  int row_count;
  int column_count;
  int generation;
};




int main()
{
  CellularAutomata cellular_automata("input.txt");

  auto total_start = chrono::system_clock::now();
  for (int i = 0; i < 100; i++)
  {
    auto start = chrono::system_clock::now();
    cellular_automata.attribute_next_generation();
    auto end = std::chrono::system_clock::now();

    chrono::duration<double> elapsed_seconds = end - start;
    time_t end_time = chrono::system_clock::to_time_t(end);

    cout << "Generation " << i + 1 << " took " << elapsed_seconds.count() << "s" << endl;
  }
  auto total_end = chrono::system_clock::now();
  printf("Total time: %f\n", chrono::duration<double>(total_end - total_start).count());

  return 0;
}
