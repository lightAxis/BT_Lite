
#include <string>
#include <algorithm>
#include <iostream>
#include <stdexcept>

char *getCmdOption(char **begin, char **end, const std::string &option)
{
    char **itr = std::find(begin, end, option);
    if (itr != end && ++itr != end)
    {
        return *itr;
    }
    return 0;
}

int main(int argc, char **argv)
{
    std::string helpStr = "-x : input tree xml file path\n"
                          "-t : input transition log file path\n"
                          "-o : output path and name\n"
                          "-m : mode of input transition log file.json or ulog\n";

    std::string input_treeXmlPath = "";
    std::string input_transitionLogPath = "";
    std::string outputPath = "";
    std::string mode = "";

    char *filename = getCmdOption(argv, argv + argc, "-x");
    if (filename)
    {
        input_treeXmlPath = filename;
    }
    filename = getCmdOption(argv, argv + argc, "-t");
    if (filename)
    {
        input_transitionLogPath = filename;
    }
    filename = getCmdOption(argv, argv + argc, "-o");
    if (filename)
    {
        outputPath = filename;
    }
    filename = getCmdOption(argv, argv + argc, "-m");
    if (filename)
    {
        mode = filename;
    }

    bool Error{false};
    if (input_treeXmlPath == "")
    {
        std::cout << "no input tree xml path" << std::endl;
        Error = true;
    }
    if (outputPath == "")
    {
        std::cout << "no output path" << std::endl;
        Error = true;
    }
    if (input_transitionLogPath == "")
    {
        std::cout << "no input transition log path" << std::endl;
        Error = true;
    }
    if (mode == "")
    {
        std::cout << "no mode detected, default is json" << std::endl;
        mode = "json";
    }

    // if (Error)
    // {
    //     std::cout << helpStr << std::endl;
    //     return 1;
    // }

    return 0;
}