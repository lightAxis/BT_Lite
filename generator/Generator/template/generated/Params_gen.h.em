@# globals
@# Params: List[str]
#pragma once

@[for param in Params]@
#include "Params/@(param).h"
@[end for]
