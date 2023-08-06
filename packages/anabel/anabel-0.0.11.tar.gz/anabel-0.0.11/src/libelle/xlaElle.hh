// include directives
#include <Element.h>
#include <Matrix.h>
#include <Vector.h>

// forward declarations
class UniaxialMaterial;

class Truss2D : public Element
{
  public:
    // constructors                                                                   
    Truss2D(int tag,
            int Nd1, int Nd2,
            UniaxialMaterial &theMaterial,
            double A);

    Truss2D();

    // destructor                                                                     
    ~Truss2D();

    // initialization
    int setDomain(Domain *theDomain);

    // public methods to obtain inforrmation about dof & connectivity                 
    int getNumExternalNodes(void) const;
    const ID &getExternalNodes(void);
    Node **getNodePtrs(void);
    int getNumDOF(void);

    // public methods to set the state of the element                                 
    int commitState(void);
    int revertToLastCommit(void);
    int revertToStart(void);
    int update(void);

    // public methods to obtain stiffness  
    const Matrix &getTangentStiff(void);
    const Matrix &getInitialStiff(void);

    // public method to obtain resisting force
    const Vector &getResistingForce(void);

    // method for obtaining information specific to an element 
    void Print(OPS_Stream &s, int flag =0);
    Response *setResponse(const char **argv, int argc, OPS_Stream &s);
    int getResponse(int responseID, Information &eleInformation);

    // public methods for database/parallel processing                                                      
    int sendSelf(int commitTag, Channel &theChannel);
    int recvSelf(int commitTag, Channel &theChannel, FEM_ObjectBroker &theBroker);
    void Print(OPS_Stream &s, int flag =0);

  protected:

  private:
    // private member functions - only available to objects of the class              
    double computeCurrentStrain(void) const;

    // private attributes - a copy for each object of the class                       
    UniaxialMaterial *theMaterial;       // pointer to a material                     
    ID  externalNodes;                   // contains the id's of end nodes            
    Matrix trans;       // hold the transformation matrix                      
    double L;           // length of truss (undeformed configuration)                                                                              
    double A;           // area of truss                                              
    Node *theNodes[2];  // node pointers                                              

    // static data - single copy for all objects of the class                         
    static Matrix trussK;   // class wide matrix for returning stiffness                            
    static Vector trussR;   // class wide vector for returning residual               
};
#endif

