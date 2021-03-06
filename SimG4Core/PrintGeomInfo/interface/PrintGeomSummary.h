#ifndef SimG4Core_PrintGeomSummary_H
#define SimG4Core_PrintGeomSummary_H

#include "SimG4Core/Watcher/interface/SimWatcher.h"
#include "SimG4Core/Notification/interface/Observer.h"
#include "DetectorDescription/Core/interface/DDSolidShapes.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
    
#include "G4NavigationHistory.hh"

#include <algorithm>
#include <iostream>
#include <vector>
#include <map>
#include <string>

class BeginOfJob;
class BeginOfRun;
class DDLogicalPart;
class G4LogicalVolume;
class G4VPhysicalVolume;
class G4VSolid;

class PrintGeomSummary : public SimWatcher,
                         public Observer<const BeginOfJob *>,
                         public Observer<const BeginOfRun *> {

public:
  PrintGeomSummary(edm::ParameterSet const & p);
  ~PrintGeomSummary();

private:
  void update(const BeginOfJob * job);
  void update(const BeginOfRun * run);
  void addSolid(const DDLogicalPart & part);
  void fillLV(G4LogicalVolume * lv);
  void dumpSummary(std::ostream& out, std::string name);
  G4VPhysicalVolume * getTopPV();
  void addName(std::string name);
  void printSummary(std::ostream & out);

private:
  std::vector<std::string>           nodeNames_;
  std::map<DDSolidShape,std::string> solidShape_;
  std::map<std::string,DDSolidShape> solidMap_;
  G4VPhysicalVolume *                theTopPV_; 
  std::vector<G4LogicalVolume*>      lvs_, touch_;
  std::vector<G4VSolid*>             sls_;
  std::map<DDSolidShape,std::pair<int,int> > kount_;
};

#endif
