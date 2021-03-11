from math import floor, fmod, sqrt
from random import randint


# 3D Gradient vectors
_GRAD3 = ((1,1,0),(-1,1,0),(1,-1,0),(-1,-1,0),
	(1,0,1),(-1,0,1),(1,0,-1),(-1,0,-1),
	(0,1,1),(0,-1,1),(0,1,-1),(0,-1,-1),
	(1,1,0),(0,-1,1),(-1,1,0),(0,-1,-1),
)

# 4D Gradient vectors
_GRAD4 = ((0,1,1,1), (0,1,1,-1), (0,1,-1,1), (0,1,-1,-1),
	(0,-1,1,1), (0,-1,1,-1), (0,-1,-1,1), (0,-1,-1,-1),
	(1,0,1,1), (1,0,1,-1), (1,0,-1,1), (1,0,-1,-1),
	(-1,0,1,1), (-1,0,1,-1), (-1,0,-1,1), (-1,0,-1,-1),
	(1,1,0,1), (1,1,0,-1), (1,-1,0,1), (1,-1,0,-1),
	(-1,1,0,1), (-1,1,0,-1), (-1,-1,0,1), (-1,-1,0,-1),
	(1,1,1,0), (1,1,-1,0), (1,-1,1,0), (1,-1,-1,0),
	(-1,1,1,0), (-1,1,-1,0), (-1,-1,1,0), (-1,-1,-1,0))

_F2 = 0.5 * (sqrt(3.0) - 1.0)
_G2 = (3.0 - sqrt(3.0)) / 6.0
_F3 = 1.0 / 3.0
_G3 = 1.0 / 6.0

class SIMPLENOISE:
    permutation = (151, 160, 137, 91, 90, 15,
                   131, 13, 201, 95, 96, 53, 194, 233, 7, 225, 140, 36, 103, 30, 69, 142, 8, 99, 37, 240, 21, 10, 23,
                   190, 6, 148, 247, 120, 234, 75, 0, 26, 197, 62, 94, 252, 219, 203, 117, 35, 11, 32, 57, 177, 33,
                   88, 237, 149, 56, 87, 174, 20, 125, 136, 171, 168, 68, 175, 74, 165, 71, 134, 139, 48, 27, 166,
                   77, 146, 158, 231, 83, 111, 229, 122, 60, 211, 133, 230, 220, 105, 92, 41, 55, 46, 245, 40, 244,
                   102, 143, 54, 65, 25, 63, 161, 1, 216, 80, 73, 209, 76, 132, 187, 208, 89, 18, 169, 200, 196,
                   135, 130, 116, 188, 159, 86, 164, 100, 109, 198, 173, 186, 3, 64, 52, 217, 226, 250, 124, 123,
                   5, 202, 38, 147, 118, 126, 255, 82, 85, 212, 207, 206, 59, 227, 47, 16, 58, 17, 182, 189, 28, 42,
                   223, 183, 170, 213, 119, 248, 152, 2, 44, 154, 163, 70, 221, 153, 101, 155, 167, 43, 172, 9,
                   129, 22, 39, 253, 9, 98, 108, 110, 79, 113, 224, 232, 178, 185, 112, 104, 218, 246, 97, 228,
                   251, 34, 242, 193, 238, 210, 144, 12, 191, 179, 162, 241, 81, 51, 145, 235, 249, 14, 239, 107,
                   49, 192, 214, 31, 181, 199, 106, 157, 184, 84, 204, 176, 115, 121, 50, 45, 127, 4, 150, 254,
                   138, 236, 205, 93, 222, 114, 67, 29, 24, 72, 243, 141, 128, 195, 78, 66, 215, 61, 156, 180)

    period = len(permutation)

    # Double permutation array so we don't need to wrap
    permutation = permutation * 2


    def snoise3(self, x, y, z, octaves, persistence, lacunarity):
        """
        Skeel Lee, 1 Jun 2014
        Method that calculates fBm using Simplex noise
        Calculations done the same way as fbm_noise3 in _simplex.c
        """
        freq = 1.0
        amp = 1.0
        max = 1.0
        total = self.noise3(x, y, z)
        for i in range(1, octaves):
            freq *= lacunarity
            amp *= persistence
            max += amp
            total += self.noise3(x * freq, y * freq, z * freq) * amp
        return total / max

    def noise3(self, x, y, z):
        """3D Perlin simplex noise.
        Return a floating point value from -1 to 1 for the given x, y, z coordinate.
        The same value is always returned for a given x, y, z pair unless the
        permutation table changes (see randomize above).
        """
        # Skew the input space to determine which simplex cell we're in
        s = (x + y + z) * _F3
        i = floor(x + s)
        j = floor(y + s)
        k = floor(z + s)
        t = (i + j + k) * _G3
        x0 = x - (i - t)  # "Unskewed" distances from cell origin
        y0 = y - (j - t)
        z0 = z - (k - t)

        # For the 3D case, the simplex shape is a slightly irregular tetrahedron.
        # Determine which simplex we are in.
        if x0 >= y0:
            if y0 >= z0:
                i1 = 1;
                j1 = 0;
                k1 = 0
                i2 = 1;
                j2 = 1;
                k2 = 0
            elif x0 >= z0:
                i1 = 1;
                j1 = 0;
                k1 = 0
                i2 = 1;
                j2 = 0;
                k2 = 1
            else:
                i1 = 0;
                j1 = 0;
                k1 = 1
                i2 = 1;
                j2 = 0;
                k2 = 1
        else:  # x0 < y0
            if y0 < z0:
                i1 = 0;
                j1 = 0;
                k1 = 1
                i2 = 0;
                j2 = 1;
                k2 = 1
            elif x0 < z0:
                i1 = 0;
                j1 = 1;
                k1 = 0
                i2 = 0;
                j2 = 1;
                k2 = 1
            else:
                i1 = 0;
                j1 = 1;
                k1 = 0
                i2 = 1;
                j2 = 1;
                k2 = 0

        # Offsets for remaining corners
        x1 = x0 - i1 + _G3
        y1 = y0 - j1 + _G3
        z1 = z0 - k1 + _G3
        x2 = x0 - i2 + 2.0 * _G3
        y2 = y0 - j2 + 2.0 * _G3
        z2 = z0 - k2 + 2.0 * _G3
        x3 = x0 - 1.0 + 3.0 * _G3
        y3 = y0 - 1.0 + 3.0 * _G3
        z3 = z0 - 1.0 + 3.0 * _G3

        # Calculate the hashed gradient indices of the four simplex corners
        perm = self.permutation
        ii = int(i) % self.period
        jj = int(j) % self.period
        kk = int(k) % self.period
        gi0 = perm[ii + perm[jj + perm[kk]]] % 12
        gi1 = perm[ii + i1 + perm[jj + j1 + perm[kk + k1]]] % 12
        gi2 = perm[ii + i2 + perm[jj + j2 + perm[kk + k2]]] % 12
        gi3 = perm[ii + 1 + perm[jj + 1 + perm[kk + 1]]] % 12

        # Calculate the contribution from the four corners
        noise = 0.0
        tt = 0.6 - x0 ** 2 - y0 ** 2 - z0 ** 2
        if tt > 0:
            g = _GRAD3[gi0]
            noise = tt ** 4 * (g[0] * x0 + g[1] * y0 + g[2] * z0)
        else:
            noise = 0.0

        tt = 0.6 - x1 ** 2 - y1 ** 2 - z1 ** 2
        if tt > 0:
            g = _GRAD3[gi1]
            noise += tt ** 4 * (g[0] * x1 + g[1] * y1 + g[2] * z1)

        tt = 0.6 - x2 ** 2 - y2 ** 2 - z2 ** 2
        if tt > 0:
            g = _GRAD3[gi2]
            noise += tt ** 4 * (g[0] * x2 + g[1] * y2 + g[2] * z2)

        tt = 0.6 - x3 ** 2 - y3 ** 2 - z3 ** 2
        if tt > 0:
            g = _GRAD3[gi3]
            noise += tt ** 4 * (g[0] * x3 + g[1] * y3 + g[2] * z3)

        return noise * 32.0
