import random
from multiprocessing import Process


def write_lines(start, end):
    with open('fa.txt', 'a') as f:
        line_count = 0
        for i in range(start, end):
            line_count += 1
            print('Process {}: {} lines written'.format(start, line_count))
            line = ''
            for j in range(2000):
                line += str(random.randint(0, 1))

            f.write(line + '\n')


if __name__ == '__main__':
    num_processes = 10
    lines_per_process = 2000 // num_processes

    processes = []
    for i in range(num_processes):
        start = i * lines_per_process
        end = (i + 1) * lines_per_process
        p = Process(target=write_lines, args=(start, end))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()
