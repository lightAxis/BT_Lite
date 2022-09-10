#pragma once

namespace BT_TEST
{
    namespace PARAM
    {
        class ParamServer
        {
        public:
            int get_b1() { return _b1; }
            int get_b2() { return _b2; }
            float get_b3() { return _b3; }
            float get_b4() { return _b4; }

            void set_b1(const int &v) { _b1 = v; }
            void set_b2(const int &v) { _b2 = v; }
            void set_b3(const float &v) { _b3 = v; }
            void set_b4(const float &v) { _b4 = v; }

        private:
            int _b1;
            int _b2;
            float _b3;
            float _b4;
        };

        static ParamServer paramServer;
    }
}