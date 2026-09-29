#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cstring>
#include <cstdlib>
#include <bitset>
#include <iomanip>

using namespace std;


// ============================================================
// Convert register name to 4-bit binary
// ============================================================
const char* get_register_bin(const char* reg_name) {

    if (strcmp(reg_name, "$zero") == 0 || strcmp(reg_name, "$zero,") == 0)
        return "0000";

    if (strcmp(reg_name, "$t0") == 0 || strcmp(reg_name, "$t0,") == 0)
        return "0001";

    if (strcmp(reg_name, "$t1") == 0 || strcmp(reg_name, "$t1,") == 0)
        return "0010";

    if (strcmp(reg_name, "$t2") == 0 || strcmp(reg_name, "$t2,") == 0)
        return "0011";

    if (strcmp(reg_name, "$t3") == 0 || strcmp(reg_name, "$t3,") == 0)
        return "0100";

    if (strcmp(reg_name, "$t4") == 0 || strcmp(reg_name, "$t4,") == 0)
        return "0101";

    if (strcmp(reg_name, "$sp") == 0 || strcmp(reg_name, "$sp,") == 0)
        return "0110";

    return "0000";
}


// ============================================================
// Convert integer to binary string
// ============================================================
void int_to_bin_string(int num, int bits, char* output) {

    // Mask keeps only the required number of bits.
    int mask = (1 << bits) - 1;
    num = num & mask;

    for (int i = bits - 1; i >= 0; i--) {
        output[bits - 1 - i] =
            (num & (1 << i)) ? '1' : '0';
    }

    output[bits] = '\0';
}


// ============================================================
// Convert 16-bit binary string to hexadecimal
// ============================================================
string binary_to_hex(const string& binary) {

    unsigned int value = bitset<16>(binary).to_ulong();

    stringstream ss;

    ss << uppercase
       << hex
       << setw(4)
       << setfill('0')
       << value;

    return ss.str();
}


// ============================================================
// MAIN
// ============================================================
int main() {

    // --------------------------------------------------------
    // Open files
    // --------------------------------------------------------

    ifstream input_file("assembly.txt");

    ofstream binary_file("machine_code.txt");

    ofstream hex_file("machine_code.hex");


    if (!input_file.is_open()) {
        cout << "Error opening assembly.txt\n";
        return 1;
    }

    if (!binary_file.is_open()) {
        cout << "Error creating machine_code.txt\n";
        return 1;
    }

    if (!hex_file.is_open()) {
        cout << "Error creating machine_code.hex\n";
        return 1;
    }


    // Logisim format
    binary_file << "v2.0 raw\n";
    hex_file << "v2.0 raw\n";


    char line[100];


    // ========================================================
    // Read assembly.txt line by line
    // ========================================================

    while (input_file.getline(line, sizeof(line))) {

        char op[10] = "";
        char arg1[15] = "";
        char arg2[15] = "";
        char arg3[15] = "";

        int parsed =
            sscanf(line, "%s %s %s %s",
                   op, arg1, arg2, arg3);


        // Empty line
        if (parsed <= 0)
            continue;


        char opcode_bin[5] = "";
        char src1_bin[5] = "";
        char src2_bin[5] = "";
        char dst_bin[5] = "";
        char imm_bin[9] = "";

        char machine_instruction[17] = "";


        // ====================================================
        // R-TYPE
        // add, sub, and, or, nor
        // ====================================================

        if (strcmp(op, "add") == 0 ||
            strcmp(op, "sub") == 0 ||
            strcmp(op, "and") == 0 ||
            strcmp(op, "or") == 0 ||
            strcmp(op, "nor") == 0) {


            if (strcmp(op, "add") == 0)
                strcpy(opcode_bin, "0001");

            else if (strcmp(op, "sub") == 0)
                strcpy(opcode_bin, "0010");

            else if (strcmp(op, "and") == 0)
                strcpy(opcode_bin, "0110");

            else if (strcmp(op, "or") == 0)
                strcpy(opcode_bin, "1111");

            else if (strcmp(op, "nor") == 0)
                strcpy(opcode_bin, "0011");


            strcpy(dst_bin,
                   get_register_bin(arg1));

            strcpy(src1_bin,
                   get_register_bin(arg2));

            strcpy(src2_bin,
                   get_register_bin(arg3));


            // Opcode | Src1 | Src2 | Dst
            sprintf(machine_instruction,
                    "%s%s%s%s",
                    opcode_bin,
                    src1_bin,
                    src2_bin,
                    dst_bin);
        }


        // ====================================================
        // SHIFT
        // sll, srl
        // ====================================================

        else if (strcmp(op, "sll") == 0 ||
                 strcmp(op, "srl") == 0) {


            if (strcmp(op, "sll") == 0)
                strcpy(opcode_bin, "0000");

            else
                strcpy(opcode_bin, "1010");


            strcpy(dst_bin,
                   get_register_bin(arg1));

            strcpy(src1_bin,
                   get_register_bin(arg2));


            int_to_bin_string(
                atoi(arg3),
                4,
                imm_bin
            );


            // Opcode | Src1 | Dst | Shift
            sprintf(machine_instruction,
                    "%s%s%s%s",
                    opcode_bin,
                    src1_bin,
                    dst_bin,
                    imm_bin);
        }


        // ====================================================
        // I-TYPE
        // addi, subi, andi, ori
        // ====================================================

        else if (strcmp(op, "addi") == 0 ||
                 strcmp(op, "subi") == 0 ||
                 strcmp(op, "andi") == 0 ||
                 strcmp(op, "ori") == 0) {


            if (strcmp(op, "addi") == 0)
                strcpy(opcode_bin, "1001");

            else if (strcmp(op, "subi") == 0)
                strcpy(opcode_bin, "1011");

            else if (strcmp(op, "andi") == 0)
                strcpy(opcode_bin, "1101");

            else
                strcpy(opcode_bin, "1110");


            strcpy(dst_bin,
                   get_register_bin(arg1));

            strcpy(src1_bin,
                   get_register_bin(arg2));


            int_to_bin_string(
                atoi(arg3),
                4,
                imm_bin
            );


            // Opcode | Src1 | Dst | Immediate
            sprintf(machine_instruction,
                    "%s%s%s%s",
                    opcode_bin,
                    src1_bin,
                    dst_bin,
                    imm_bin);
        }


        // ====================================================
        // BRANCH
        // beq, bneq
        // ====================================================

        else if (strcmp(op, "beq") == 0 ||
                 strcmp(op, "bneq") == 0) {


            if (strcmp(op, "beq") == 0)
                strcpy(opcode_bin, "1100");

            else
                strcpy(opcode_bin, "0100");


            strcpy(src1_bin,
                   get_register_bin(arg1));

            strcpy(dst_bin,
                   get_register_bin(arg2));


            int_to_bin_string(
                atoi(arg3),
                4,
                imm_bin
            );


            // Opcode | Src1 | Src2 | Immediate
            sprintf(machine_instruction,
                    "%s%s%s%s",
                    opcode_bin,
                    src1_bin,
                    dst_bin,
                    imm_bin);
        }


        // ====================================================
        // LOAD / STORE
        // lw, sw
        // ====================================================

        else if (strcmp(op, "lw") == 0 ||
                 strcmp(op, "sw") == 0) {


            if (strcmp(op, "lw") == 0)
                strcpy(opcode_bin, "0101");

            else
                strcpy(opcode_bin, "0111");


            char base_reg[10] = "";
            int offset = 0;


            // Example:
            // lw $t1 4($t2)
            //
            // Extract:
            // offset = 4
            // base_reg = $t2

            sscanf(arg2,
                   "%d($9)",
                   &offset);


            // More reliable parsing of offset(base)
            char* open = strchr(arg2, '(');
            char* close = strchr(arg2, ')');

            if (open && close) {

                offset = atoi(arg2);

                int length =
                    close - open - 1;

                strncpy(
                    base_reg,
                    open + 1,
                    length
                );

                base_reg[length] = '\0';
            }


            strcpy(dst_bin,
                   get_register_bin(arg1));

            strcpy(src1_bin,
                   get_register_bin(base_reg));


            int_to_bin_string(
                offset,
                4,
                imm_bin
            );


            // Opcode | Dst | Base | Offset
            sprintf(machine_instruction,
                    "%s%s%s%s",
                    opcode_bin,
                    src1_bin,
                    dst_bin,
                    imm_bin);
        }


        // ====================================================
        // JUMP
        // j
        // ====================================================

        else if (strcmp(op, "j") == 0) {

            strcpy(opcode_bin, "1000");


            int_to_bin_string(
                atoi(arg1),
                8,
                imm_bin
            );


            // Opcode | 8-bit Address | 0000
            sprintf(machine_instruction,
                    "%s%s0000",
                    opcode_bin,
                    imm_bin);
        }


        // ====================================================
        // Unknown instruction
        // ====================================================

        else {

            cout << "Unknown instruction: "
                 << op << endl;

            continue;
        }


        // ====================================================
        // WRITE BINARY
        // ====================================================

        binary_file
            << machine_instruction
            << '\n';


        // ====================================================
        // CONVERT BINARY → HEX
        // ====================================================

        string binary(machine_instruction);

        string hex =
            binary_to_hex(binary);


        // ====================================================
        // WRITE HEX
        // ====================================================

        hex_file
            << hex
            << '\n';
    }


    // ========================================================
    // Close files
    // ========================================================

    input_file.close();

    binary_file.close();

    hex_file.close();


    cout << "\nCompilation successful!\n";
    cout << "Created: machine_code.txt\n";
    cout << "Created: machine_code.hex\n";


    return 0;
}