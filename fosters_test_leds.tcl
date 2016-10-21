
puts "========== BEGIN FOSTERS TEST_LEDS =========="

mifpga_wr 0 0xfc 0x80
brd_ctrl_wr 0xf8 0x22200a80

set g_on 	0x00000001
set g_blink 0x00000002
set y_on 	0x00000004
set y_blink 0x00000008

for {set curr_port 1} {$curr_port <= 32} {incr curr_port} {

	exec led_util -portmask 0xffffffff;# all port LEDs off

	# get the right register for reading led_util and mifpga_rd
	# ports 1-8   reg = 0x2a0
	# ports 9-16  reg = 0x300
	# ports 17-24 reg = 0x360
	# ports 25-32 reg = 0x3c0


	# test ports 1-8
	if {$curr_port < 9} {
		set reg 0x2a0
		set bit_shift [expr ($curr_port - 1) * 4]

		# test solid green
		exec led_util -port $curr_port -green 1;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $g_on << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : solid green failed     \n Value=$reg_value   Correct Value=$working"
		}

		#test blinking green
		exec led_util -port $curr_port -green 2;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $g_blink << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : blinking green failed  \n Value=$reg_value   Correct Value=$working"
		}

		#test solid yellow
		exec led_util -port $curr_port -yellow 1;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $y_on << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : solid yellow failed    \n Value=$reg_value   Correct Value=$working"
		}

		#test blinking yellow
		exec led_util -port $curr_port -yellow 2;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $y_blink << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : blinking yellow failed \n Value=$reg_value   Correct Value=$working"
		}

	# test ports 9-16
	} elseif {$curr_port > 8 && $curr_port < 17} {
		set reg 0x300
		set bit_shift [expr ($curr_port % 9) * 4]

		# test solid green
		exec led_util -port $curr_port -green 1;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $g_on << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : solid green failed     \n Value=$reg_value   Correct Value=$working"
		}

		#test blinking green
		exec led_util -port $curr_port -green 2;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $g_blink << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : blinking green failed  \n Value=$reg_value   Correct Value=$working"
		}

		#test solid yellow
		exec led_util -port $curr_port -yellow 1;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $y_on << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : solid yellow failed    \n Value=$reg_value   Correct Value=$working"
		}

		#test blinking yellow
		exec led_util -port $curr_port -yellow 2;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $y_blink << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : blinking yellow failed \n Value=$reg_value   Correct Value=$working"
		}

	# test ports 17-24
	} elseif {$curr_port > 16 && $curr_port < 25} {
		set reg 0x360
		set bit_shift [expr ($curr_port % 17) * 4]

		# test solid green
		exec led_util -port $curr_port -green 1;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $g_on << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : solid green failed     \n Value=$reg_value   Correct Value=$working"
		}

		#test blinking green
		exec led_util -port $curr_port -green 2;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $g_blink << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : blinking green failed  \n Value=$reg_value   Correct Value=$working"
		}

		#test solid yellow
		exec led_util -port $curr_port -yellow 1;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $y_on << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : solid yellow failed    \n Value=$reg_value   Correct Value=$working"
		}

		#test blinking yellow
		exec led_util -port $curr_port -yellow 2;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $y_blink << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : blinking yellow failed \n Value=$reg_value   Correct Value=$working"
		}

	# test ports 25-32
	} else {
		set reg 0x3c0
		set bit_shift [expr ($curr_port % 25) * 4]

		# test solid green
		exec led_util -port $curr_port -green 1;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $g_on << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : solid green failed     \n Value=$reg_value   Correct Value=$working"
		}

		#test blinking green
		exec led_util -port $curr_port -green 2;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $g_blink << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : blinking green failed  \n Value=$reg_value   Correct Value=$working"
		}

		#test solid yellow
		exec led_util -port $curr_port -yellow 1;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $y_on << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : solid yellow failed    \n Value=$reg_value   Correct Value=$working"
		}

		#test blinking yellow
		exec led_util -port $curr_port -yellow 2;
		set reg_value [mifpga_rd 0 $reg]

		set working [expr $y_blink << $bit_shift]
		if {$reg_value != $working} {
			puts "Port $curr_port : blinking yellow failed \n Value=$reg_value   Correct Value=$working"
		}
	}
}

exec led_util -portmask 0xffffffff;
puts "================ END OF TEST ================ "

