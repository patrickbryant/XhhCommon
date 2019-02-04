#include "xAODJet/JetContainer.h"
#include "xAODJet/JetContainerInfo.h"
#include "xAODBTagging/BTagging.h"
#include "xAODJet/Jet.h"
#include "xAODJet/JetAttributes.h"

#include <EventLoop/Worker.h>
#include <XhhCommon/Helpers.h>

float MV2(const xAOD::Jet* jet, std::string flavor){

  if (flavor != "MV2c00" && 
      flavor != "MV2c10" && 
      flavor != "MV2c100" && 
      flavor != "MV2c20"){
    return -100;
  }

  double discriminant = -99;
  const xAOD::BTagging *btag = jet->btagging();
  btag->MVx_discriminant(flavor, discriminant);

  return float(discriminant);
}

bool came_from_b_quark(const xAOD::TruthParticle* part){
  //there is a memory leak here
  int n_parents = part->nParents();
  if(n_parents == 0){
    return false;
  }

  for(int i=0; i<n_parents; i++){
    const xAOD::TruthParticle* curr_parent = part->parent(i);

    if(!curr_parent){
      //delete curr_parent;
      continue;
    }

    if(abs(curr_parent->pdgId()) == 5 && curr_parent->status() == 23){
      return true;
    }

    bool decision = came_from_b_quark(curr_parent);

    if(decision)
      return true;
  }

  return false;
}

bool has_b_hadron_child(const xAOD::TruthParticle* part){
  int n_children = part->nChildren();

  for(int i=0; i<n_children; i++){
    const xAOD::TruthParticle* curr_child = part->child(i);

    if(curr_child->isBottomHadron()){
      return true;
    }
  }

  return false;
}

bool svtx_inside_jet(double x, double y, double z, const xAOD::Vertex* pv, const xAOD::Jet* jet, double dR_thresh){
  double dx = x ;
  double dy = y ;
  double dz = z ;

  if(x < -99999.){
    return false;
  }

  if(pv){
    dx = x - pv->x();
    dy = y - pv->y();
    dz = z - pv->z();
  }

  double phi = TMath::ATan2(dy, dx);
  double theta = TMath::ATan2(fabs(dy), dz);

  double eta = -TMath::Log(TMath::Tan(theta/2.0));

  double jet_eta = jet->eta();
  double jet_phi = jet->phi();

  double my_dR = dR(eta, phi, jet_eta, jet_phi);

  //std::cout << "dx: " << dx << " dy: " << dy << " dz: " << dz << " theta: " << theta << " tan(theta/2): " << TMath::Tan(theta/2.0) << " eta: " << eta << " phi: " << phi << " dR: " << dR << std::endl;

  return (my_dR < dR_thresh);
}

//int count_vertices(std::vector<double> x_vert, std::vector<double> y_vert, std::vector<double> z_vert, const xAOD::Vertex* pv, const xAOD::Jet* jet, double dR_thresh){
int count_vertices(std::vector<double> x_vert, std::vector<double> y_vert, std::vector<double> z_vert, const xAOD::Jet* jet, double dR_thresh){

  //const xAOD::Vertex* origin = jet->getAssociatedObject<xAOD::Vertex>(xAOD::JetAttribute::OriginVertex);
  //  std::cout << "SIZE: " << origins.size();
  
  int num_vert = x_vert.size();
  int ret = 0;
  for(int i=0; i<num_vert; i++){
    if(svtx_inside_jet(x_vert[i], y_vert[i], z_vert[i], 0, jet, dR_thresh)){
      ret++;
    }
  }

  return ret;
}

int count_bquarks(std::vector<double> eta, std::vector<double> phi, std::vector<int> pdgid, const xAOD::Jet* jet, double dR_thresh){
  int num_part = eta.size();

  int ret = 0;
  for(int i=0; i<num_part; i++){
    if(abs(pdgid[i]) != 5){
      continue;
    }

    double dR = TMath::Sqrt(TMath::Power(eta[i]-jet->eta(), 2) + TMath::Power(phi[i]-jet->phi(), 2));

    if(dR < dR_thresh) ret++;
  }

  return ret;
}
float dphi(float phi1, float phi2) {
    float PHI = fabs(phi1-phi2);
    if (PHI<=TMath::Pi())
        return PHI;
    else
        return 2*TMath::Pi()-PHI;
}

float dR(float eta1, float phi1, float eta2, float phi2) {
    float _deta = eta1 - eta2;
    float _dphi = dphi(phi1, phi2);
    return sqrt(_deta*_deta + _dphi*_dphi);
}

float dR_vertices(float x1, float y1, float z1, float x2, float y2, float z2){

  double phi1 = TMath::ATan2(y1, x1);
  double theta1 = TMath::ATan2(fabs(y1), z1);
  double eta1 = -TMath::Log(TMath::Tan(theta1/2.0));

  double phi2 = TMath::ATan2(y2, x2);
  double theta2 = TMath::ATan2(fabs(y2), z2);
  double eta2 = -TMath::Log(TMath::Tan(theta2/2.0));

  return dR(eta1, phi1, eta2, phi2);
}

int MV2_benchmark(const xAOD::Jet* jet, std::string flavor, int name){

  // https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/BTaggingBenchmarks
  // https://twiki.cern.ch/twiki/bin/viewauth/AtlasProtected/Run2JetMoments

  // -1: not evaluated
  //  0: fail MV2 benchmark
  //  1: pass MV2 benchmark

  if (flavor != "MV2c20"){
    return -1;
  }

  if (name != 90 && 
      name != 85 && 
      name != 80 && 
      name != 77 && 
      name != 70 && 
      name != 60 && 
      name != 50 && 
      name != 30){
    return -1;
  }

  float score = MV2(jet, flavor);
  int radius = jet->getSizeParameter()*10;

  if (radius == 2 && jet->getInputType() == xAOD::JetInput::Track){
    if (name == 30) return (score >  0.9321);
    if (name == 50) return (score >  0.6055);
    if (name == 60) return (score >  0.1899);
    if (name == 70) return (score > -0.3098);
    if (name == 77) return (score > -0.6134);
    if (name == 80) return (score > -0.7132);
    if (name == 85) return (score > -0.8433);
    if (name == 90) return (score > -0.9291);
  }

  if (radius == 3 && jet->getInputType() == xAOD::JetInput::Track){
    if (name == 30) return (score >  0.9455);
    if (name == 50) return (score >  0.6720);
    if (name == 60) return (score >  0.2872);
    if (name == 70) return (score > -0.2343);
    if (name == 77) return (score > -0.5787);
    if (name == 80) return (score > -0.6932);
    if (name == 85) return (score > -0.8397);
    if (name == 90) return (score > -0.9301);
  }

  if (radius == 4 && jet->getInputType() == xAOD::JetInput::EMTopo){
    if (name == 30) return (score >  0.9540);
    if (name == 50) return (score >  0.7535);
    if (name == 60) return (score >  0.4496);
    if (name == 70) return (score > -0.0436);
    if (name == 77) return (score > -0.4434);
    if (name == 80) return (score > -0.5911);
    if (name == 85) return (score > -0.7887);
    if (name == 90) return (score > -0.9185);
  }

  return -1;
}
