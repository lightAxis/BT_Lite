@# em_globals
@#'NAMESPACE': str
@#'Params_Dict': Dict[str, str] (Name, Type)
@#
#pragma once

namespace @(NAMESPACE)
{
    namespace PARAM
    {
        class ParamServer
        {
        public:
@[for name in Params_Dict.keys()]@
            @(Params_Dict[name]) get_@(name)() { return _@(name); }
@[end for]
@[for name in Params_Dict.keys()]@
            @(Params_Dict[name]) set_@(name)(const @(Params_Dict[name]) &v) { _@(name) = v; }
@[end for]
        private:
@[for name in Params_Dict.keys()]@
            @(Params_Dict[name]) _@(name);
@[end for]
        };

        static ParamServer paramServer;
    }
}