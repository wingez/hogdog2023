#include <stdio.h>

typedef struct {double x; double y;} coordinate2d_t;

coordinate2d_t coord_array[5] = 
   {{10, 1.0},
    {20, 4.1},
    {30,9.2}, 
    {40,10.33}, 
    {50,23.2}};

//Takes coordinate_array, certain x and size of coord_array
double interpolate(coordinate2d_t *coord_array, int n, double x) {
    double x_diff = 0;
    double consec_diff = 0;
    
    for(int i = 0; i < n-1; i++) { //loops through array
        //checks if requested x val is between 2 cosecutive values
        if (coord_array[i].x <= x && coord_array[i+1].x >= x ) { 
            x_diff = x - coord_array[i].x;
            consec_diff = coord_array[i+1].x - coord_array[i].x;
            //returns lowerbound + linear interpolation
            return coord_array[i].y + (coord_array[i+1].y - coord_array[i].y) * x_diff/consec_diff; 
        }
    }

    return -1; //neg for illegal interpolation 
}

int main() {
    double x = 35;
    double y = interpolate(coord_array,5,x);

    printf("For array of (x,y): \n");
    for(int i = 0; i < 5; i++){
        printf("(%.2lf, %.2lf)\n", coord_array[i].x, coord_array[i].y);
    }

    printf("The interpolated value for (x,y) = (%lf,%lf)\n",x,y);
}

