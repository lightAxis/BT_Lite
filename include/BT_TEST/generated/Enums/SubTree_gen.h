#pragma once

namespace BT_TEST
{
    enum class SubTree
    {
        // Groot
        RootTree = 0,

        // Custom
        CustomSubTree1 = 1,
        CustomSubTree2 = 2,
    };

    namespace Cvt
    {
        char *getSubTreeName(SubTree subtree)
        {
            switch (subtree)
            {
            case SubTree::RootTree:
                return const_cast<char *>("RootTree");
            case SubTree::CustomSubTree1:
                return const_cast<char *>("CustomSubTree1");
            case SubTree::CustomSubTree2:
                return const_cast<char *>("CustomSubTree2");
            }
            return const_cast<char *>("None");
        }
    }
}