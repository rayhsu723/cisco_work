/********************************************************************
 * tableintr.cpp
 * 
 * Created on: August 4, 2016
 * Name: Alan Way, Raymond Hsu
 *
 * Copyright 2016 Cisco Systems. All rights reserved.
 *
 * *****************************************************************/
#include "armintr_common.h"

typedef struct _archintr_table_t {
	char *name;
	uint32 sup_ok_isr_a;
	uint32 sts_r_a;
} archintr_table_t;

archintr_table_t alta_archintr_table = {
    "Alta",                 //name
    0x130,                  //sup_ok_isr_a
    0x0304                  //sts_r_a
};

archintr_table_t blackcomb_archintr_table = {
	"Blackcomb",            //name
	0x118,                  //sup_ok_isr_a
	0x0304                  //sts_r_a
};

archintr_table_t bretton_archintr_table = {
    "Bretton",              //name
    0x218,                  //sup_ok_isr_a
    0x08C                   //sts_r_a
};

archintr_table_t bristolmt_archintr_table = {
	"BristolMt",            //name
	0x118, 		            //sup_ok_isr_a
	0x304				    //sts_r_a
};

archintr_table_t canyons_archintr_table = {
    "Canyons",              //name
    0x218,                  //sup_ok_isr_a
    0x08C                   //sts_r_a
};

archintr_table_t cascade_archintr_table = {
    "Cascade",              //name
    0x218,                  //sup_ok_isr_a
    0x08C                   //sts_r_a
};

archintr_table_t cypress_archintr_table =  {
	"Cypress",              //name
	0x118,                  //sup_ok_isr_a
	0x304                   //sts_r_a
};

archintr_table_t fujimt_archintr_table = {
	"FujiMt",            	//name
	0x118, 		            //sup_ok_isr_a
	0x304   			    //sts_r_a
};

archintr_table_t honeycomb_archintr_table = {
	"Honeycomb",            //name
	0x118,                  //sup_ok_isr_a
	0x304                   //sts_r_a
};

archintr_table_t mammoth_archintr_table = {
    "Mammoth",              //name
    0x218,                  //sup_ok_isr_a
    0x08C                   //sts_r_a
};

archintr_table_t moena_archintr_table = {
	"Moena",                //name
	0x118,                  //sup_ok_isr_a
	0x304                   //sts_r_a
};

archintr_table_t montage_archintr_table = {
	"Montage",              //name
	0x118,                  //sup_ok_isr_a
	0x304                   //sts_r_a
};

archintr_table_t mtbaldy_archintr_table = {
	"MtBaldy",				//name
    0x118,                  //sup_ok_isr_a
    0x304                   //sts_r_a
};

archintr_table_t mtkato_archintr_table = {
    "MtKato",               //name
    0x218,                  //sup_ok_isr_a
    0x08C                   //sts_r_a
};

archintr_table_t mtrose_archintr_table = {
	"MtRose",               //name
    0x118,                  //sup_ok_isr_a
    0x304                   //sts_r_a
};

archintr_table_t seymour_archintr_table = {
	"Seymour",              //name
    0x118,                  //sup_ok_isr_a
    0x304                   //sts_r_a
};

archintr_table_t shasta_archintr_table =  {
	"Shasta",               //name
    0x118,                  //sup_ok_isr_a
    0x304                   //sts_r_a
};

archintr_table_t shawnee_archintr_table = {
    "Shawnee",              //name
    0x218,                  //sup_ok_isr_a
    0x08C                   //sts_r_a
};

archintr_table_t sierra_archintr_table = {
	"Sierra",				//name
    0x118,                  //sup_ok_isr_a
    0x304                   //sts_r_a
};

archintr_table_t sugarloaf_archintr_table =  {
	"SUGARLOAF",            //name
    0x118,                  //sup_ok_isr_a
    0x304                   //sts_r_a
};

archintr_table_t whistler_archintr_table = {
	"Whistler",             //name
    0x118,                  //sup_ok_isr_a
    0x304                   //sts_r_a
};

uint32 new_sup_ok_clear_ints(archintr_table_t brd_table)
{
    uint32 temp = 0;
    uint32 rc = DIAG_SUCCESS;

    brd_ctrl_wr(brd_table.sup_ok_isr_a, 0);
    brd_ctrl_rd(brd_table.sup_ok_isr_a, &temp);

    /* Ignore SUP OK Error Interrupt. Can happen due to no SUP2 */
    if(temp & 0x1E)
    {
        CLI("ERROR: Unable to clear interrupt on %s IO-FPGA 0x%08x = 0x%08x\n", brd_table.name, brd_table.sup_ok_isr_a, temp);
        brd_ctrl_rd(brd_table.sts_r_a, &temp);
        CLI("ERROR: %s IO-FPGA Board Status 0x%08x = 0x%08x\n", brd_table.name, brd_table.sts_r_a, temp);
        rc = ARMINTR_CLEAR_INTS_ERROR;
    }

    return rc;
}

uint32 new_sup_ok_check_ints(archintr_table_t brd_table)
{
    uint32 temp = 0;
    uint32 temp2 = 0;
    uint32 rc = DIAG_SUCCESS;
    char err_str[500];

    brd_ctrl_rd(brd_table.sup_ok_isr_a, &temp);
    brd_ctrl_rd(brd_table.sts_r_a, &temp2);

    /* Expect only OK Change Interrupt */
    if( (temp & 0x1E) == 0x10)
    {
        CLI("%s Detected SUP_OK_CHANGE Interrupt. 0x%08x\n", brd_table.name, temp);
    }
    else
    {
        sprintf(err_str, "ERROR: %s did not detect SUP OK change STS 0x%08x = 0x%08x, ISR 0x%08x = 0x%08x => ", brd_table.name, brd_table.sts_r_a, temp2, brd_table.sup_ok_isr_a, temp);
        if(temp & 0x04)
        {
            strcat(err_str, "SUP_OK_MISMATCH ");
            /* SW Workaround for FPGA debounce. This ensures that mismatch doesn't occur */
            if( (((temp2 & 0x00000500)>>8) ^ ((temp2 & 0x00000A00)>>9)) == 0)
            {
                CLI("SW %s Detected SUP_OK_CHANGE Interrupt. 0x%08x\n", brd_table.name, temp);
                rc = DIAG_SUCCESS;
                goto cleanup;
            }
        }
        else if(temp & 0x08) {
            strcat(err_str, "WHICH_ACTIVE_MISMATCH ");
        }
        else if(temp & 0x02) {
            strcat(err_str, "SUP_ACTIVE_CHANGE ");
        }
        CLI("%s\n", err_str);
        rc = ARMITNR_SUPOK_ERROR;
    }
	cleanup:        
    	return rc;
}

uint32 new_sup_which_active_clear_ints(archintr_table_t brd_table)
{
    uint32 temp = 0;
    uint32 rc = DIAG_SUCCESS;

    brd_ctrl_wr(brd_table.sup_ok_isr_a, 0);
    brd_ctrl_rd(brd_table.sup_ok_isr_a, &temp);
    
    /* Ignore SUP OK Error Interrupt. Can happen due to no SUP2 */
    if(temp & 0x3E)
    {
        CLI("ERROR: Unable to clear interrupt on %s IO-FPGA 0x%08x = 0x%08x\n", brd_table.name, brd_table.sup_ok_isr_a, temp);
        brd_ctrl_rd(brd_table.sts_r_a, &temp);
        CLI("ERROR: %s IO-FPGA SC Status 0x%08x = 0x%08x\n", brd_table.name, brd_table.sts_r_a, temp);
        rc = ARMINTR_CLEAR_INTS_ERROR;
    }

    return rc;
}

uint32 new_sup_which_active_check_ints(archintr_table_t brd_table)
{
    uint32 temp = 0;
    uint32 temp2 = 0;
    uint32 rc = DIAG_SUCCESS;
    char err_str[500];

    brd_ctrl_rd(brd_table.sup_ok_isr_a, &temp);
    brd_ctrl_rd(brd_table.sup_ok_isr_a, &temp2);

    /* Expect only Active Change Interrupt */
    if( (temp & 0x3e) == 0x02)
    {
        CLI("%s Detected SUP_ACTIVE_CHANGE Interrupt. 0x%08x\n", brd_table.name, temp);
    }
    else
    {
        sprintf(err_str, "ERROR: %s did not detect SUP ACTIVE change STS 0x%08x = 0x%08x, ISR 0x%08x = 0x%08x => ", brd_table.name, brd_table.sts_r_a, temp2, brd_table.sup_ok_isr_a, temp);
        if(temp & 0x08)
            strcat(err_str, "WHICH_ACTIVE_MISMATCH ");
        else if((temp & 0x02) == 0)
            strcat(err_str, "NO_SUP_ACTIVE_CHANGE ");


        CLI("%s\n", err_str);
        rc = ARMITNR_SUPOK_ERROR;
    }
    return rc;
}

