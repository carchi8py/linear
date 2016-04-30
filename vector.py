from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'

    # Create a vector
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
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
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def magnitude(self):
        coordinates_squared = [x**2 for x in self.coordinates]
        return sqrt(sum(coordinates_squared))

    def normalized(self):
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/Decimal(magnitude))
        except ZeroDivisionError:
            raise Exception(CANNOT_NORMALIZE_ZERO_VECTOR_MSG)

    def dot(self, v):
        """
        Compute the DOT product
        """
        return sum([x*y for x,y in zip(self.coordinates, v.coordinates)])
    def angle_with(self, v, in_degrees=False):
        print 'hi'
        try:
            u1 = self.normalized()
            print u1
            u2 = v.normalized()
            print u2
            angle_in_radians = acos(u1.dot(u2))

            if in_degrees:
                degrees_per_radians = 180. / pi
                return angle_in_radians * degrees_per_radians
            else:
                return angle_in_radians
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e

    #Print the vector
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    #Check if 2 vectors are equal
    def __eq__(self, v):
        return self.coordinates == v.coordinates
