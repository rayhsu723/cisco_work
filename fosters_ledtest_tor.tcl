puts "\n========== BEGIN LEDTEST-TOR FOR FOSTERS ==========\n"


set type [list "FRONT_BCN" "FRONT_STATUS_RED" "FRONT_STATUS_GREEN" "FRONT_ENV_RED" "FRONT_ENV_GREEN" "REAR_BCN" "REAR_STATUS_RED" "REAR_STATUS_GREEN" "FAN4" "FAN3" "FAN2" "FAN1" "PORT" "ALL"]

# set led_setting [list "blink" "on" "off"]

for {set i 0} {$i < [llength $type]} {incr i} {
	puts "\n"
	brd_ctrl_wr 0x80 0x0


	# test front beacon LED (same as back beacon LED)
	if {[lindex $type $i] == "FRONT_BCN"} {
		ledtest-tor FRONT_BCN
		set correct_value 0x80000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: led-test FRONT_BCN blink : value = $value 	correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_BCN blink PASS"
		}

		ledtest-tor FRONT_BCN on
		set correct_value 0x40000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_BCN on : value = $value 	correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_BCN on PASS"
		}

		ledtest-tor FRONT_BCN off
		set correct_value  0x00000000
		set correct_value2 0xc0000000
		set value [brd_ctrl_rd 0x80]
		if {($correct_value == $value) || ($correct_value2 == $value)} {
			puts "ledtest-tor FRONT_BCN off PASS"
		} else {
			puts "ERROR: ledtest-tor FRONT_BCN off : value = $value  correct_value = $correct_value OR $correct_value2"
		}





	} elseif {[lindex $type $i] == "FRONT_STATUS_RED"} {
		ledtest-tor FRONT_STATUS_RED
		set correct_value 0x20000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_STATUS_RED blink : value = $value  correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_STATUS_RED blink PASS"
		}

		ledtest-tor FRONT_STATUS_RED on
		set correct_value 0x10000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_STATUS_RED on : value = $value 	correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_STATUS_RED on PASS"
		}

		ledtest-tor FRONT_STATUS_RED off
		set correct_value 0x00000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_STATUS_RED off : value = $value  correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_STATUS_RED off PASS"
		}





	} elseif {[lindex $type $i] == "FRONT_STATUS_GREEN"} {
		ledtest-tor FRONT_STATUS_GREEN
		set correct_value 0x08000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_STATUS_GREEN blink : value = $value  correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_STATUS_GREEN blink PASS"
		}

		ledtest-tor FRONT_STATUS_GREEN on
		set correct_value 0x04000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_STATUS_GREEN on : value = $value 	correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_STATUS_GREEN on PASS"
		}

		ledtest-tor FRONT_STATUS_GREEN off
		set correct_value 0x00000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_STATUS_GREEN off : value = $value  correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_STATUS_GREEN off PASS"
		}





	} elseif {[lindex $type $i] == "FRONT_ENV_RED"} {
		ledtest-tor FRONT_ENV_RED
		set correct_value 0x02000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_ENV_RED blink : value = $value  correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_ENV_RED blink PASS"
		}

		ledtest-tor FRONT_ENV_RED on
		set correct_value 0x01000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_ENV_RED on : value = $value 	correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_ENV_RED on PASS"
		}

		ledtest-tor FRONT_ENV_RED off
		set correct_value  0x03000000
		set correct_value2 0x00000000
		set value [brd_ctrl_rd 0x80]
		if {($correct_value == $value) || ($correct_value2 == $value)} {
			puts "ledtest-tor FRONT_ENV_RED off PASS"
		} else {
			puts "ERROR: ledtest-tor FRONT_ENV_RED off : value = $value  correct_value = $correct_value OR $correct_value2"
		}





	} elseif {[lindex $type $i] == "FRONT_ENV_GREEN"} {
		ledtest-tor FRONT_ENV_GREEN
		set correct_value 0x00800000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_ENV_GREEN blink : value = $value  correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_ENV_GREEN blink PASS"
		}

		ledtest-tor FRONT_ENV_GREEN on
		set correct_value 0x00400000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor FRONT_ENV_GREEN on : value = $value 	correct_value = $correct_value"
		} else {
			puts "ledtest-tor FRONT_ENV_GREEN on PASS"
		}

		ledtest-tor FRONT_ENV_GREEN off
		set correct_value  0x00c00000
		set correct_value2 0x00000000
		set value [brd_ctrl_rd 0x80]
		if {($correct_value == $value) || ($correct_value2 == $value)} {
			puts "ledtest-tor FRONT_ENV_GREEN off PASS"
		} else {
			puts "ERROR: ledtest-tor FRONT_ENV_GREEN off : value = $value  correct_value = $correct_value OR $correct_value2"
		}





	} elseif {[lindex $type $i] == "REAR_STATUS_RED"} {
		ledtest-tor REAR_STATUS_RED
		set correct_value 0x00080000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor REAR_STATUS_RED blink : value = $value  correct_value = $correct_value"
		} else {
			puts "ledtest-tor REAR_STATUS_RED blink PASS"
		}

		ledtest-tor REAR_STATUS_RED on
		set correct_value 0x00040000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor REAR_STATUS_RED on : value = $value 	correct_value = $correct_value"
		} else {
			puts "ledtest-tor REAR_STATUS_RED on PASS"
		}

		ledtest-tor REAR_STATUS_RED off
		set correct_value 0x00000000
		set value [brd_ctrl_rd 0x80]
		if {$correct_value != $value} {
			puts "ERROR: ledtest-tor REAR_STATUS_RED off : value = $value  correct_value = $correct_value"
		} else {
			puts "ledtest-tor REAR_STATUS_RED off PASS"
		}





	} elseif {[lindex $type $i] == "PORT"} {
		ledtest-tor PORT off
		set reg [list 0x2a0 0x300 0x360 0x3c0]

		ledtest-tor PORT blink green
		set correct_value 0x22222222
		foreach offset $reg {
			set value [mifpga_rd 0 $offset]
			if {$correct_value != $value} {
				puts "ERROR: ledtest-tor PORT blink green : offset = $offset  value = $value  correct_value = $correct_value"
			} else {
				puts "ledtest-tor PORT blink green : offest = $offset PASS"
			}
		}

		ledtest-tor PORT on green
		set correct_value 0x11111111
		foreach offset $reg {
			set value [mifpga_rd 0 $offset]
			if {$correct_value != $value} {
				puts "ERROR: ledtest-tor PORT on green : offset = $offset  value = $value  correct_value = $correct_value"
			} else {
				puts "ledtest-tor PORT blink green : offest = $offset PASS"
			}
		}

		ledtest-tor PORT blink yellow
		set correct_value 0x88888888
		foreach offset $reg {
			set value [mifpga_rd 0 $offset]
			if {$correct_value != $value} {
				puts "ERROR: ledtest-tor PORT blink yellow : offset = $offset  value = $value  correct_value = $correct_value"
			} else {
				puts "ledtest-tor PORT blink yellow : offest = $offset PASS"
			}
		}

		ledtest-tor PORT on yellow
		set correct_value 0x44444444
		foreach offset $reg {
			set value [mifpga_rd 0 $offset]
			if {$correct_value != $value} {
				puts "ERROR: ledtest-tor PORT on yellow : offset = $offset  value = $value  correct_value = $correct_value"
			} else {
				puts "ledtest-tor PORT on yellow : offest = $offset PASS"
			}
		}

		ledtest-tor PORT off
		set correct_value 0x00000000
		foreach offset $reg {
			set value [mifpga_rd 0 $offset]
			if {$correct_value != $value} {
				puts "ERROR: ledtest-tor PORT off : offset = $offset  value = $value  correct_value = $correct_value"
			} else {
				puts "ledtest-tor PORT off : offest = $offset PASS"
			}
		}





	} elseif {[lindex $type $i] == "FAN4"} {
		fan-led instmask=0x8 led_color=0
		fan-led instmask=0x8 led_color=1
		fan-led instmask=0x8 led_color=2
		fan-led instmask=0x8 led_color=3
		puts "FAN4 fan-led PASS"





	} elseif {[lindex $type $i] == "FAN3"} {
		fan-led instmask=0x4 led_color=0
		fan-led instmask=0x4 led_color=1
		fan-led instmask=0x4 led_color=2
		fan-led instmask=0x4 led_color=3
		puts "FAN3 fan-led PASS"





	} elseif {[lindex $type $i] == "FAN2"} {
		fan-led instmask=0x2 led_color=0
		fan-led instmask=0x2 led_color=1
		fan-led instmask=0x2 led_color=2
		fan-led instmask=0x2 led_color=3
		puts "FAN2 fan-led PASS"





	} elseif {[lindex $type $i] == "FAN1"} {
		fan-led instmask=0x1 led_color=0
		fan-led instmask=0x1 led_color=1
		fan-led instmask=0x1 led_color=2
		fan-led instmask=0x1 led_color=3
		puts "FAN1 fan-led PASS"
	}

} 

puts "\n=========== END LEDTEST-TOR FOR FOSTERS ==========="