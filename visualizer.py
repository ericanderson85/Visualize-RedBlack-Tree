import pygame
import pygame.gfxdraw


class Visualizer:
    def __init__(self, tree, time_delay_ms):
        self.tree = tree
        self.time_delay_ms = time_delay_ms
        self.width = 1200
        self.height = 800
        self.node_radius = 30
        self.font_size = 24
        self.vertical_spacing = 80

        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Red-Black Tree Visualizer")
        self.clock = pygame.time.Clock()
        self.last_switch_time = pygame.time.get_ticks()

        self.font = pygame.font.SysFont('Arial', self.font_size)

        self.input_active = True
        self.input_text = ''
        self.playing_snapshots = False
        self.tree_snapshots = []
        self.snapshot_index = 0

    def draw_tree(self, node, x, y, horizontal_spacing):
        if node is None:
            return

        node_color = (255, 0, 0) if node.color else (0, 0, 0)

        pygame.gfxdraw.aacircle(self.screen, int(
            x), int(y), self.node_radius, node_color)
        pygame.gfxdraw.filled_circle(self.screen, int(
            x), int(y), self.node_radius, node_color)

        text_surface = self.font.render(str(node.data), True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(x, y))
        self.screen.blit(text_surface, text_rect)

        if node.left:
            self._draw_edge_and_child(
                node.left, x, y, horizontal_spacing, left=True)

        if node.right:
            self._draw_edge_and_child(
                node.right, x, y, horizontal_spacing, left=False)

    def _draw_edge_and_child(self, child_node, parent_x, parent_y, horizontal_spacing, left):
        offset = -horizontal_spacing if left else horizontal_spacing
        child_x = parent_x + offset
        child_y = parent_y + self.vertical_spacing
        pygame.draw.aaline(
            self.screen,
            (0, 0, 0),
            (parent_x, parent_y + self.node_radius),
            (child_x, child_y - self.node_radius)
        )
        self.draw_tree(child_node, child_x, child_y, horizontal_spacing / 2)

    def run(self):
        running = True
        while running:
            self.clock.tick(60)
            current_time = pygame.time.get_ticks()

            self._handle_events()

            self.screen.fill((255, 255, 255))

            if self.playing_snapshots:
                self._play_snapshots(current_time)
            else:
                self._display_current_tree()

            self._draw_input_box()

            pygame.display.flip()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif self.input_active and event.type == pygame.KEYDOWN:
                self._handle_keydown(event)

    def _handle_keydown(self, event):
        if event.key == pygame.K_RETURN:
            self._process_input()
        elif event.key == pygame.K_BACKSPACE:
            self.input_text = self.input_text[:-1]
        else:
            self.input_text += event.unicode

    def _process_input(self):
        try:
            value = int(self.input_text)
            if not self.tree.contains(self.tree.root, value):
                self.tree.insert(value)
                self.tree_snapshots = list(self.tree.snapshots)
                self.tree.snapshots.clear()
                self.playing_snapshots = True
                self.snapshot_index = 0
                self.last_switch_time = pygame.time.get_ticks()
        except ValueError:
            print("Invalid input")
        self.input_text = ''

    def _play_snapshots(self, current_time):
        if current_time - self.last_switch_time >= self.time_delay_ms:
            self.snapshot_index += 1
            self.last_switch_time = current_time
            if self.snapshot_index >= len(self.tree_snapshots):
                self.playing_snapshots = False

        if self.snapshot_index < len(self.tree_snapshots):
            current_tree = self.tree_snapshots[self.snapshot_index]
            if current_tree.root:
                self.draw_tree(
                    current_tree.root,
                    x=self.width // 2,
                    y=100,
                    horizontal_spacing=self.width // 4
                )

    def _display_current_tree(self):
        if self.tree.root:
            self.draw_tree(
                self.tree.root,
                x=self.width // 2,
                y=100,
                horizontal_spacing=self.width // 4
            )

    def _draw_input_box(self):
        input_box_rect = pygame.Rect(10, self.height - 50, 200, 40)
        pygame.draw.rect(self.screen, (200, 200, 200), input_box_rect)
        input_text_surface = self.font.render(self.input_text, True, (0, 0, 0))
        self.screen.blit(input_text_surface,
                         (input_box_rect.x + 5, input_box_rect.y + 5))
