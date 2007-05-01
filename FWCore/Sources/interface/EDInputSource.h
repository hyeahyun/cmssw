#ifndef Framework_EDInputSource_h
#define Framework_EDInputSource_h

/*----------------------------------------------------------------------
$Id: EDInputSource.h,v 1.6 2007/03/04 06:00:22 wmtan Exp $
----------------------------------------------------------------------*/

#include "DataFormats/Provenance/interface/LuminosityBlockID.h"
#include "DataFormats/Provenance/interface/RunID.h"
#include "FWCore/Framework/interface/InputSource.h"
#include "FWCore/Catalog/interface/FileCatalog.h"
#include <vector>
#include <string>

namespace edm {
  class InputSourceDescription;
  class ParameterSet;
  class EDInputSource : public InputSource {
  public:
    explicit EDInputSource(ParameterSet const& pset, InputSourceDescription const& desc);
    virtual ~EDInputSource();

    std::vector<std::string> const& logicalFileNames() const {return catalog_.logicalFileNames();}
    std::vector<std::string> const& fileNames() const {return catalog_.fileNames();}
    std::vector<FileCatalogItem> const& fileCatalogItems() const {return catalog_.fileCatalogItems();}
    InputFileCatalog& catalog() {return catalog_;}

  private:
    virtual void setRun(RunNumber_t);
    virtual void setLumi(LuminosityBlockNumber_t lb);
    
    InputFileCatalog catalog_;
  };
}
#endif
