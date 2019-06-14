import numpy as np


def straight_line_with_line_intersect(straight_line, line):
    v1 = np.array(straight_line.end_position) - straight_line.start_position
    v2 = np.array(line.start_position) - straight_line.start_position
    v3 = np.array(line.end_position) - straight_line.start_position
    det1 = v1[0] * v2[1] - v1[1] * v2[0]
    det2 = v1[0] * v3[1] - v1[1] * v3[0]
    return (det1 < 0 < det2) or (det1 > 0 > det2) or det1 == 0 or det2 == 0


def lines_intersect(line1, line2):
    return straight_line_with_line_intersect(line1, line2) and straight_line_with_line_intersect(line2, line1)


def rotate_vector(vector, angle):
    theta = np.radians(angle)
    c, s = np.cos(theta), np.sin(theta)
    return np.dot(np.array(((c, -s), (s, c))), vector)


def point_from_line_square_distance(point, line):
    x_diff, y_diff = line.end_position[0] - line.start_position[0], line.end_position[1] - line.start_position[1]
    det = line.start_position[0] * line.end_position[1] - line.start_position[1] * line.end_position[0]
    return (y_diff * point[0] - x_diff * point[1] - det) ** 2 / (x_diff ** 2 + y_diff ** 2)


def line_width(line):
    return np.linalg.norm(np.array(line.end_position) - line.start_position)


def point_to_line_projection(point, line):
    v1 = point - np.array(line.start_position)
    v2 = line.end_position - np.array(line.start_position)
    return np.dot(v1, v2) / (np.linalg.norm(v2) ** 2) * v2


def lines_intersection_point(line1, line2):
    x1, x2, x3, x4 = line1.start_position[0], line1.end_position[0], line2.start_position[0], line2.end_position[0]
    y1, y2, y3, y4 = line1.start_position[1], line1.end_position[1], line2.start_position[1], line2.end_position[1]
    det1 = x1 * y2 - y1 * x2
    det2 = x3 * y4 - y3 * x4
    det3 = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    x_point = (det1 * (x3 - x4) - (x1 - x2) * det2) / det3
    y_point = (det1 * (y3 - y4) - (y1 - y2) * det2) / det3
    return np.array([x_point, y_point])


def lines_equal_direction(line1, line2):
    v1 = line1.end_position - np.array(line1.start_position)
    v2 = line2.end_position - np.array(line2.start_position)
    return np.dot(v1, v2) > 0


def lines_parallel(line1, line2):
    v1 = line1.end_position - np.array(line1.start_position)
    v2 = line2.end_position - np.array(line2.start_position)
    return v1[0] * v2[1] - v1[1] * v2[0] == 0
