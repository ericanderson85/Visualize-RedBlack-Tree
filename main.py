from visualizer import Visualizer
from red_black_tree import RedBlackTree


def main():
    red_black_tree = RedBlackTree()
    visualizer = Visualizer(tree=red_black_tree, time_delay_ms=1000)
    visualizer.run()


if __name__ == '__main__':
    main()
