// Public Good Games on square lattice 
// cooperator contributes c=1 cost to every game 
// game is played among G=5 members 
//                                         2 May, 2009

#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <string.h>

#define L           400      // lattice size                   
#define SIZE        (L*L)    // number of players
#define MC_STEPS    200000   // run-time in MCS     
#define r           5.00    // multiplicative factor 
#define K           0.50    // temperature
#define NAMEOUT     "r5_00"
#define RANDOMIZE   4521

typedef int       tomb1[SIZE];
typedef long int  tomb3[SIZE][4];
typedef long int  tomb4[2];

tomb1 player_s;   // matrix, contains players' strategies 
tomb3 player_n;   // matrix, contains players' neighbours
tomb4 Spop;       // fraction of strategies                 

void prodgraph(void); // creates connectivity graph                   
void initial(void);   // random initial state                        

/********************** for RNG ************************************/
/* Period parameters */  
#define NN 624
#define MM 397
#define MATRIX_A 0x9908b0df   /* constant vector a */
#define UPPER_MASK 0x80000000 /* most significant w-r bits */
#define LOWER_MASK 0x7fffffff /* least significant r bits */

/* Tempering parameters */   
#define TEMPERING_MASK_B 0x9d2c5680
#define TEMPERING_MASK_C 0xefc60000
#define TEMPERING_SHIFT_U(y)  (y >> 11)
#define TEMPERING_SHIFT_S(y)  (y << 7)
#define TEMPERING_SHIFT_T(y)  (y << 15)
#define TEMPERING_SHIFT_L(y)  (y >> 18)

static unsigned long mt[NN]; /* the array for the state vector  */
static int mti=NN+1; /* mti==NN+1 means mt[NN] is not initialized */

/* Initializing the array with a seed */
void sgenrand(seed)
    unsigned long seed; 
{
    int i;

    for (i=0;i<NN;i++) {
         mt[i] = seed & 0xffff0000;
         seed = 69069 * seed + 1;
         mt[i] |= (seed & 0xffff0000) >> 16;
         seed = 69069 * seed + 1;
    }
    mti = NN;
}

void lsgenrand(seed_array)
    unsigned long seed_array[];
    /* the length of seed_array[] must be at least NN */
{
    int i;

    for (i=0;i<NN;i++) 
      mt[i] = seed_array[i];
    mti=NN;
}

double genrand() 
/* generating unsigned long */
{
    unsigned long y;
    static unsigned long mag01[2]={0x0, MATRIX_A};
    /* mag01[x] = x * MATRIX_A  for x=0,1 */

    if (mti >= NN) { /* generate N words at one time */
        int kk;

        if (mti == NN+1)   /* if sgenrand() has not been called, */
            sgenrand(4357); /* a default initial seed is used   */

        for (kk=0;kk<NN-MM;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+MM] ^ (y >> 1) ^ mag01[y & 0x1];
        }
        for (;kk<NN-1;kk++) {
            y = (mt[kk]&UPPER_MASK)|(mt[kk+1]&LOWER_MASK);
            mt[kk] = mt[kk+(MM-NN)] ^ (y >> 1) ^ mag01[y & 0x1];
        }
        y = (mt[NN-1]&UPPER_MASK)|(mt[0]&LOWER_MASK);
        mt[NN-1] = mt[MM-1] ^ (y >> 1) ^ mag01[y & 0x1];

        mti = 0;
    }
  
    y = mt[mti++];
    y ^= TEMPERING_SHIFT_U(y);
    y ^= TEMPERING_SHIFT_S(y) & TEMPERING_MASK_B;
    y ^= TEMPERING_SHIFT_T(y) & TEMPERING_MASK_C;
    y ^= TEMPERING_SHIFT_L(y);

    return y;  /* for integer generation */
}

double randf()
/* generating reals  */
{
  return ( (double)genrand() * 2.3283064370807974e-10 );
}

long randi(LIM)
/* generating integer */
{
 return((unsigned long)genrand() % LIM);
}
/**************** END of RNG ******************************/
			   
void initial(void)
{
 int i,strat1;
 
  for (i=0; i<SIZE; i++) // random initial distribution of strategies
  { 
    strat1 = (int) randi(2);
    player_s[i] = strat1;
    Spop[strat1]++;
  }
} // initial 

void prodgraph(void)             
// define neighbors on square lattice 
{ int nneighbor, iu, ju, neighbor1, neighbor2;
  long int rewire, first, player1,player2,player3,MCe;
  double x;
  int i,j;
 
  // set an initial square lattice-like neighborhood
  for(i=0; i<L; i++)                     
  {
   for(j=0; j<L; j++)
    { 
      player1 = L * j + i;              /* consider a site >> a player */

      iu = i + 1;         ju = j;     if (iu==L) iu = 0;
      player2 = L * ju + iu;  player_n[player1][0] = player2;

      iu = i;             ju = j + 1; if (ju==L) ju = 0;
      player2 = L * ju + iu;  player_n[player1][1] = player2;

      iu = i - 1;         ju = j;     if (i==0) iu = L - 1;
      player2 = L * ju + iu;  player_n[player1][2] = player2;

      iu = i;             ju = j - 1; if (j==0) ju = L - 1;
      player2 = L * ju + iu;  player_n[player1][3] = player2;
    }
  }

} /* prodgraph */

int main()
{
int ri,source,target,nbh,nbs,n_nbs,n_nbh,contrib0,contrib;
float P_source,P_target,adaptation_rate,dP;
long int i;
int strat1, strat2,sn,snn;
long int player1,player2;
long int steps;

  FILE *fout;
  char outname[25];
  
//  sprintf(outname,"%s.dat",NAMEOUT);
  sgenrand(RANDOMIZE); // initialize RNG 

  prodgraph();  // creates connectivity graph 

  for (i=0; i<2; i++) { Spop[i] = 0; }  // portion of strategies 
  initial();    // strategy distribution

  for (steps=0; steps<MC_STEPS; steps++)
  {
    for (i=0; i<SIZE; i++)
    {
      player1 = (int) randi(SIZE);      // choose a source 
      strat1 = player_s[player1];       // strategy of source 
      ri = (int) randi(4);
      player2 = player_n[player1][ri];  // target site
      strat2 = player_s[player2];       // strategy of target

      if (strat1!=strat2)            // different strategies 
      {
       P_source = 0; P_target = 0;
       
       contrib0 = strat1;           // source contribution to 0th game
       for (nbh=0; nbh<4; nbh++)
       {
         nbs = player_n[player1][nbh];   // neighbor of source 
	 sn = player_s[nbs];            // strategy of neighbor 

         contrib0 += sn; // neighbor's contribution to 0th game
         contrib = sn;   // neighbor's contribution to his/her own game
         for (n_nbh=0; n_nbh<4; n_nbh++)
         {
           n_nbs = player_n[nbs][n_nbh];   // neighbor of nbs 
	   snn = player_s[n_nbs];          // strategy of neighbor of nbs
	   contrib += snn;                 
	 }
	 P_source += (r*contrib)/5-strat1;
       } // nbh	 	 
       P_source += (r*contrib0)/5-strat1; 

       contrib0 = strat2;           // target contribution to 0th game
       for (nbh=0; nbh<4; nbh++)
       {
         nbs = player_n[player2][nbh];   // neighbor of source 
	 sn = player_s[nbs];            // strategy of neighbor 

         contrib0 += sn; // neighbor's contribution to 0th game
         contrib = sn;   // neighbor's contribution to his/her own game
         for (n_nbh=0; n_nbh<4; n_nbh++)
         {
           n_nbs = player_n[nbs][n_nbh];   // neighbor of nbs 
	   snn = player_s[n_nbs];          // strategy of neighbor of nbs
	   contrib += snn;                 
	 }
	 P_target += (r*contrib)/5-strat2;
       } // nbh	 	 
       P_target += (r*contrib0)/5-strat2; 
       
       adaptation_rate = 1.0 / (1.0 + exp((P_target-P_source)/K));
       
       if (randf() < adaptation_rate)
        {
	 player_s[player2] = player_s[player1];
	 Spop[strat1]++;
	 Spop[strat2]--;
        }
      } // different players       
    } // i: elementary MC step
    if ((steps%500) == 0)
    {
      fout = fopen(outname,"a+");
      int theNumb = 0;
      for(i = 0; i < SIZE; i ++){
      	theNumb += player_s[i];
      }
//      fprintf(fout,"%d%6.3f\n",steps,(float)Spop[1]/SIZE);
      printf("%d%6.3f\n",steps,(float)theNumb/SIZE);
      fclose(fout); 
    }
  } // MC step
  return 0;
} // main 

