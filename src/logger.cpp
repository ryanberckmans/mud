#include "logger.hpp"

void Logger::log( const string msg, const int channel, const int lvl ) {
	if ( lvl <= _log_level ) {		
		for( int i = 0 ; i < lvl ; i++ ) {
			out << " ";
		}

		map<int, string>::iterator it = channels.find( channel);
		
		if ( it != channels.end()) {
			out << "[" << it->second << "] ";
		}

		out << msg << endl;		
	}
}

void Logger::log( const string msg, const int channel ) {
	log( msg, channel, _log_level );
}

void Logger::log( const string msg ) {
	log( msg, CHANNEL_NONE, _log_level );
}

void Logger::log( const char* const msg, const int channel, const int lvl) {
	log( string(msg), channel, lvl );
}

void Logger::log( const char* const msg, const int channel ) {
	log( string(msg), channel, _log_level);
}
void Logger::log( const char* const msg ) {
	log( string(msg), CHANNEL_NONE, _log_level);
}

boost::shared_ptr<Logger> Logger::inst;

boost::shared_ptr<Logger> Logger::instance(const int level ) {
	if ( inst.get() == 0 ) {
		inst.reset( new Logger(cout, level ) );
	}

	return inst;
}

Logger::Logger( ostream& out, const int level ) : out(out), _log_level(level) {
	channels[SS] = string("SS");
    channels[CR] = string("CR");
    channels[PY] = string("PY");
    channels[AC] = string("AC");
}
