#include <string>

#include "include/io.hpp"
#include "include/population.hpp"
#include "include/problem.hpp"
#include "include/problems/hock_schittkowsky_71.hpp"

using namespace pagmo;

struct so_ind_comparison 
{
	bool operator() (vector_double a,vector_double b) { return (a[0]<b[0]);}
};

int main()
{
    // Constructing a population
    problem prob{hock_schittkowsky_71{}};
    population pop{prob, 10};
    print(pop);
    print(pop.get_best_idx(2,so_ind_comparison()));
    
}