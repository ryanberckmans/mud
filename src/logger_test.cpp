#include <string>
#include <sstream>
#include "logger.h"

int main( int argc) {

	Logger::instance()->log( "Hey" );

	LOG(SS, "HeyHigh");
	LOG_MED(0, "HeyMED");
	LOG_LOW(0, "HeyLOW KSDFSDFLJSDLFKS");

	LOG(SS, "argc: " << argc);	
	cin.get();
}