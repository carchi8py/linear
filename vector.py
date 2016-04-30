from math import sqrt, acos, pi
from decimal import Decimal, getcontext

getcontext().prec = 30

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL = "There is no Unique Parallel"
    NO_UNIQUE_ORTHOGONAL = "There is no unique Orthogonal"
    ONLY_WORKS_FOR_2_3 = "Only works for 2 or 3 "

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
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            #Sometime we sould get just slight over 1, or under 1. this prevent that
            temp = u1.dot(u2)
            if temp > 1.0:
                temp = Decimal('1.0')
            if temp < -1.0:
                temp = Decimal('-1.0')
            angle_in_radians = acos(temp)

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
    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    def is_parallel_to(self, v):
        return ( self.is_zero() or v.is_zero() or self.angle_with(v) == 0 or self.angle_with(v) == pi)

    def is_zero(self, tolerance=1e-10):
        return self.magnitude() < tolerance

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self. NO_UNIQUE_PARALLEL:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL)
            else:
                raise e
    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL)
            else:
                raise e

    def cross(self, v):
        try:
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            new_coordinates = [y_1*z_2 - y_2*z_1,
                                -(x_1*z_2 - x_2*z_1),
                                x_1*y_2 - x_2*y_1 ]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 vaules to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many vaules to unpack' or msg == 'need more than 1 vaule to unpack'):
                raise Exception(self.ONLY_WORKS_FOR_2_3)
            else:
                raise e

    def area_of_triangle_with(self, v):
        return Decimal(self.area_of_parallelogram_with(v)) / Decimal('2.0')

    def area_of_parallelogram_with(self, v):
        cross_product = self.cross(v)
        return cross_product.magnitude()

    #Print the vector
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    #Check if 2 vectors are equal
    def __eq__(self, v):
        return self.coordinates == v.coordinates
