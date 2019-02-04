#ifndef Helpers_Helpers_H
#define Helpers_Helpers_H

#include "xAODTruth/TruthParticle.h"
#include "xAODTruth/TruthVertex.h"
#include "xAODTracking/Vertex.h"
#include <functional>

float MV2(const xAOD::Jet* jet, std::string flavor);
int   MV2_benchmark(const xAOD::Jet* jet, std::string flavor, int name);
float dphi(float phi1, float phi2);
float dR(float eta1, float phi1, float eta2, float phi2);
float dR_vertices(float x1, float y1, float z1, float x2, float y2, float z2);
bool came_from_b_quark(const xAOD::TruthParticle* p);
bool has_b_hadron_child(const xAOD::TruthParticle* p);
template <class T> struct sort_pt : std::binary_function <T,T,bool> {
  bool operator() (T* x, T* y) const {return x->pt()>y->pt();}
};
bool svtx_inside_jet(double x, double y, double z, const xAOD::Vertex* pv, const xAOD::Jet* jet, double dR_thresh);
//int count_vertices(std::vector<double> x_vert, std::vector<double> y_vert, std::vector<double> z_vert, const xAOD::Vertex* pv, const xAOD::Jet* jet, double dR_thresh = 0.2);
int count_vertices(std::vector<double> x_vert, std::vector<double> y_vert, std::vector<double> z_vert, const xAOD::Jet* jet, double dR_thresh = 0.2);
int count_bquarks(std::vector<double> eta, std::vector<double> phi, std::vector<int> pdgid, const xAOD::Jet* jet, double dR_thresh = 0.2);



#endif
