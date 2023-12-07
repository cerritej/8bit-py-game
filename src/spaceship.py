class Spaceship:
    def __init__(self, name, x, y, width, height):
        self.__name = name
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        if not name:
            raise ValueError("Name cannot be blank.")
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        if len(name) > 255:
            raise ValueError("Name cannot be over 255 chars.")
        self.__name = name

    @property
    def x(self):
        return self.__x

    @x.setter
    def x(self, x):
        # Add any validation if needed
        self.__x = x

    @property
    def y(self):
        return self.__y

    @y.setter
    def y(self, y):
        self.__y = y

    @property
    def width(self):
        return self.__width

    @width.setter
    def width(self, width):
        self.__width = width

    @property
    def height(self):
        return self.__height

    @height.setter
    def height(self, height):
        self.__height = height

    def move(self, dx, dy):
        self.__x += dx
        self.__y += dy
