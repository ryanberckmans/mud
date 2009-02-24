
#include <iostream>

using namespace std;

class None {};

template< typename T> class Physical : public T
{

public:
  Physical() : _room(0) {}

  void room( const int room ) { _room = room; }
  int room() { return _room; }

private:
  int _room;

};


template< typename T> class Alive : public T
{
public:

  Alive() : _hp(0) {}

  void damage( const int damage ) { _hp -= damage; if (_hp < 0) { cout << "DEAD!!" << endl; } }

  void heal( const int heal ) { damage( -1 * heal ); }

  void hp( const int hp ) { _hp = hp; }
  int hp() { return _hp; }

private:
  int _hp;
};

template< typename T> class HasZone : public T
{

public:
  
  HasZone() : _zone(99) {}

  void zone( const int zone) { _zone = zone; }
  int zone() { return _zone; }

private:

  int _zone;


};

class Bob {
public:
  void bar() { cout << "Bar" << endl; }


};

template< typename T> class Combat : public T
{

public:
  Combat() {

    // Using global io_service
    // Register this for combat

  }

};

typedef Alive< Physical< HasZone< None>  > > Mob;
typedef Physical< HasZone< None> > Object;
typedef HasZone< None > Room;
//typedef Combat< Alive>



template< typename T> class Big : public T {

public:
  void foo() { cout << "Foo" << endl; }


};


int main() {

  Big<Bob> c;

  c.foo();
  c.bar();

  Mob m;

  m.damage( 10 ) ;
  m.heal( 11 );
  m.damage( 10 );
  cout << m.room() << endl;
  m.room( 10 );
  cout << m.room() << endl;

  Object o;
  Room r;


}
