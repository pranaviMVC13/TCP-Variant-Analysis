
global defaultRNG
$defaultRNG seed 0

#Create a simulator object
set ns [new Simulator]

#Default Protocols to Tahoe and CBR Rate.
set arg0 Tahoe
set arg1 Tahoe
set arg2 1 

#Read arguments
if {$argc == 3} {
	set arg0 [expr [lindex $argv 0]]
	set arg1 [expr [lindex $argv 1]]
	set arg2 [expr [lindex $argv 2]]
}

#Set simulation environment
set fastLink 12Mb
set slowLink 12Mb
set shortDelay 5ms
set longDelay 40ms
set qSize [expr {125}]
set flowTime 100.0
set runTime 110.0
set overhead 0


set cbrRate $arg2
append cbrRate mb


set nf [open tcpEvaluation.nam w]
$ns namtrace-all $nf
set prefix ./trFiles/
append prefix $arg0
append prefix _
append prefix $arg1
append prefix _
append prefix $arg2
append prefix Mbps

set tf [open $prefix w]
$ns trace-all $tf


proc finish {} {
        global ns nf tf
        $ns flush-trace	
        close $nf		
        close $tf
        exit 0
}

# creates nodes and links between them
set n0 [$ns node]
set n1 [$ns node]
set n2 [$ns node]
set n3 [$ns node]
set n4 [$ns node]
set n5 [$ns node]



$ns duplex-link $n0 $n1 $fastLink $shortDelay DropTail
$ns duplex-link $n4 $n1 $fastLink $shortDelay DropTail
$ns duplex-link $n1 $n2 $fastLink $longDelay DropTail
$ns duplex-link $n2 $n3 $fastLink $shortDelay DropTail
$ns duplex-link $n2 $n5 $fastLink $shortDelay DropTail


$ns queue-limit $n1 $n2 $qSize
 

$ns color 0 Red	
$ns color 1 Blue
$ns color 2 Green
		
$ns duplex-link-op $n0 $n1 orient right-down
$ns duplex-link-op $n4 $n1 orient right-up
$ns duplex-link-op $n1 $n2 orient right
$ns duplex-link-op $n2 $n3 orient right-up
$ns duplex-link-op $n2 $n5 orient right-down


$ns duplex-link-op $n1 $n2 queuePos 0.5

# Create a TCP sending agent and attach it to A
if ([string equal $arg0 Tahoe]) {
	set tcp0 [new Agent/TCP]
} elseif ([string equal $arg0 Cubic]) {
	
        set tcp0 [new Agent/TCP/Linux]
	set select_tcp "$tcp0 select_ca cubic"
	append select_tcp $arg0
	$ns at 0 $select_tcp
} elseif ([string equal $arg0 Reno]) {
	
        set tcp0 [new Agent/TCP/Linux]
	set select_tcp "$tcp0 select_ca reno"
	append select_tcp $arg0
	$ns at 0 $select_tcp
} else {
        set tcp0 [new Agent/TCP/$arg0]
	
}

$tcp0 set fid_ 0
$tcp0 set class_ 0
$tcp0 set window_ 1000
if ([string equal $arg0 Vegas]) {
	$tcp0 set packetSize_ 1000
} else {
	$tcp0 set packetSize_ 960
}
$tcp0 set overhead_ $overhead
$ns attach-agent $n0 $tcp0


$tcp0 attach $tf
$tcp0 tracevar cwnd_

#Create a TCP receive agent (a traffic sink) and attach it to n4
set end0 [new Agent/TCPSink/Sack1]
$ns attach-agent $n3 $end0
$ns connect $tcp0 $end0  


set ftp1 [new Application/FTP]
$ftp1 attach-agent $tcp0

# Create second TCP sending agent and attach it to A
if ([string equal $arg1 Tahoe]) {
	set tcp1 [new Agent/TCP]
} elseif ([string equal $arg1 Cubic]) {
	
        set tcp1 [new Agent/TCP/Linux]
	set select_tcp "$tcp1 select_ca cubic"
	append select_tcp $arg1
	$ns at 0 $select_tcp
} elseif ([string equal $arg1 Reno]) {
	
        set tcp1 [new Agent/TCP/Linux]
	set select_tcp "$tcp1 select_ca reno"
	append select_tcp $arg1
	$ns at 0 $select_tcp
} else {
        set tcp1 [new Agent/TCP/$arg1]
	
}

$tcp1 set fid_ 1
$tcp1 set class_ 1
$tcp1 set window_ 1000
if ([string equal $arg1 Vegas]) {
	$tcp1 set packetSize_ 1000
} else {
	$tcp1 set packetSize_ 960
}
$tcp1 set overhead_ $overhead
$ns attach-agent $n4 $tcp1


$tcp1 attach $tf
$tcp1 tracevar cwnd_

#Create a TCP receive agent (a traffic sink) and attach it to n5
set end1 [new Agent/TCPSink/Sack1]
$ns attach-agent $n5 $end1
$ns connect $tcp1 $end1 


set ftp2 [new Application/FTP]
$ftp2 attach-agent $tcp1
set udp [new Agent/UDP]
$udp set fid_ 2
$ns attach-agent $n1 $udp
set end2 [new Agent/Null]
$ns attach-agent $n2 $end2
$ns connect $udp $end2
set cbr [new Application/Traffic/CBR]
$cbr set type_ CBR
$cbr set packet_size_ 1000
$cbr set rate_ $cbrRate
$cbr set random_ 1
$cbr attach-agent $udp


$ns at 0.0 "$ftp1 start"
$ns at 0.0 "$ftp2 start"
$ns at 0.0 "$cbr start"
$ns at $flowTime "$ftp1 stop"
$ns at $flowTime "$ftp2 stop"
$ns at $flowTime "$cbr stop"
$ns at $runTime "finish"

#Run the simulation
$ns run
