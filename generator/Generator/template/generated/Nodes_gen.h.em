@# globals
@# Actions: List[str]
@# Conditions = List[str]
@# Controls = List[str]
@# Decorators = List[str]
@# SubTrees = List[str]
#pragma once

// Actions
@[for action in Actions]@
#include "Actions/@(action).h"
@[end for]
// Conditions
@[for condition in Conditions]@
#include "Conditions/@(condition).h"
@[end for]
// Controls
@[for control in Controls]@
#include "Controls/@(control).h"
@[end for]
// Decorators
@[for decorator in Decorators]@
#include "Decorators/@(decorator).h"
@[end for]
// SubTrees
@[for subtree in SubTrees]@
#include "SubTrees/@(subtree).h"
@[end for]