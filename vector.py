from math import sqrt

class Vector(object):
    # Create a vector
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def plus(self, v):
        """
        Add 2 vectors together
        """
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        #another way to do this
        #new_coordinates =[]
        #n = len(self.coordinates)
        #for i in range(n)
        #   new_coordinates.append(self.coordinates[i], v.coordinates[i])
        return Vector(new_coordinates)

    def minus(self, v):
        """
        Minus 2 vectors together
        """
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def times_scalar(self, c):
        """
        Mulipiles a vector by a scalar
        """
        new_coordinates = [c*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(1./magnitude)
        except ZeroDivisionError:
            raise Exception('Cannot normalize the zero vector')

    #Print the vector
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    #Check if 2 vectors are equal
    def __eq__(self, v):
        return self.coordinates == v.coordinates
