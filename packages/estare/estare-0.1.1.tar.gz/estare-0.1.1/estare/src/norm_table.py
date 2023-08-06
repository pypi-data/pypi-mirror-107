
import numpy as np


converter = 180.0 / np.pi
        
def angle_table( x_range, y_range ):
    angle = np.zeros( (x_range, y_range), dtype=float)
    norm_table = np.zeros_like(angle)
    
    for i in range(x_range):
        x_comp = i*i
        for j in range(y_range):
            y_comp = j*j
            tmp_norm = np.sqrt(x_comp + y_comp)
            angle[i, j] = converter*np.arccos( i / tmp_norm )
            norm_table[i, j] = tmp_norm

    return norm_table, angle


if __name__ == '__main__':
    x_range = 2000
    y_range = 4000

    norm_matrix, angle_matrix = angle_table( x_range, y_range )
    np.save('../aux/norm_matrix.npy', norm_matrix)
    np.save('../aux/angle_table.npy', angle_matrix)
