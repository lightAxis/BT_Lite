#pragma once

#include "Enums.h"
#include "Nodes.h"
#include "Params.h"

namespace BT_TEST
{

    class test__
    {
    public:
        test__(PARAM::PARAM_b1<false> b1) : _b1(b1) {}
        ~test__() = default;

        int getB1() { return _b1.get(); }

    private:
        PARAM::PARAM_b1<false> _b1;
    };
    class test_
    {
    public:
        test_(PARAM::PARAM_b1<true> b1) : _b1(b1) {}
        ~test_() = default;

        int getB1() { return _b1.get(); }

    private:
        PARAM::PARAM_b1<true> _b1;
    };

    static void test()
    {
        PARAM::PARAM_b1<false> b1;
        PARAM::PARAM_b1<true> b1_;
        PARAM::PARAM_b1<true> b1__;

        b1.set(43);
        b1_.set(56);

        printf("nor : %d, blackb : %d, linkedBlackb : %d \n", b1.get(), b1_.get(), b1__.get());

        test_ test1(b1_);
        test_ test2(b1__);
        printf("test1 : %d, test2 : %d\n", test1.getB1(), test2.getB1());

        test__ test3(b1);
        b1.set(4);
        test__ test4(b1);
        printf("test3 : %d, test4 : %d \n", test3.getB1(), test4.getB1());
    }
}