

class BeastGame(QuestGame):
    player_sprite_image = resolve_resource_path("images/boy_simple.png")
    screen_width = 500
    screen_height = 500
    left_viewport_margin = 96                            
    right_viewport_margin = 96
    bottom_viewport_margin = 96
    top_viewport_margin = 96
    player_initial_x = 300
    player_initial_y = 300
    player_speed = 8
    num_blocks = 1

    def setup_maps(self):
        """Sets up the standard island map.
        """
        super().setup_maps()
        sprite_classes = {
            "Obstacles": Wall,
            "Background": QuestSprite,
        }
        self.add_map(TiledMap(resolve_resource_path("images/island/island.tmx"), sprite_classes))

class PushableBlock(QuestSprite):


class TerrainGenerator:
    """
    A class to generate random initial configurations of terrain. The current
    implementation is a very simple version--it just provides a random
    scattering of terrain. But terrain generation is a deep and complex topic; 
    `TerrainGenerator` could be subclassed to make it more complex. For example, 
    it might be nice to have terrain "seed" in clusters. 

        from arcade import SpriteList
        from quest.map import GridArea

        game.terrain = SpriteList()
        area = GridArea(0, 0, 50, 50)
        gen = TerrainGenerator(area, 20)
        for point in gen:
            x, y = point
            hill = 
            game.terrain.append(Box
            


    Advanced: Iterator
    ------------------
    You already know how to work with lists. Now let's expand that idea out a
    bit and consider iterators. To "iterate" means to go through something one
    by one. Some structures are iterable even though they can't fit into lists.
    For example, you can go through the natural numbers (0, 1, 2, 3, ...) one by
    one for as long as you like. But natural numbers obviously can't fit into a
    list--they're infinitely large and it would crash your computer if you
    tried!

    This is where iterators come in handy. They work like lists, but they're
    lazy and only iterate over their contents when they absolutely have to.
    That's a nice way to handle infinitely large collections, or collections
    which get generated on demand. This will be our strategy for terrain
    generation. The `TerrainGenerator` is responsible for 
    """

    def __iter__(self):
        """
        """
        self.terrain = []
        return self

    def __next__(self):
