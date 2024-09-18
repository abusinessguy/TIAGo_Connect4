// Generated by gencpp from file move_decision/Move.msg
// DO NOT EDIT!


#ifndef MOVE_DECISION_MESSAGE_MOVE_H
#define MOVE_DECISION_MESSAGE_MOVE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace move_decision
{
template <class ContainerAllocator>
struct Move_
{
  typedef Move_<ContainerAllocator> Type;

  Move_()
    : column(0)
    , TurnCounter(0)
    , winner(0)
    , player(0)  {
    }
  Move_(const ContainerAllocator& _alloc)
    : column(0)
    , TurnCounter(0)
    , winner(0)
    , player(0)  {
  (void)_alloc;
    }



   typedef int32_t _column_type;
  _column_type column;

   typedef int32_t _TurnCounter_type;
  _TurnCounter_type TurnCounter;

   typedef int32_t _winner_type;
  _winner_type winner;

   typedef int32_t _player_type;
  _player_type player;





  typedef boost::shared_ptr< ::move_decision::Move_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::move_decision::Move_<ContainerAllocator> const> ConstPtr;

}; // struct Move_

typedef ::move_decision::Move_<std::allocator<void> > Move;

typedef boost::shared_ptr< ::move_decision::Move > MovePtr;
typedef boost::shared_ptr< ::move_decision::Move const> MoveConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::move_decision::Move_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::move_decision::Move_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::move_decision::Move_<ContainerAllocator1> & lhs, const ::move_decision::Move_<ContainerAllocator2> & rhs)
{
  return lhs.column == rhs.column &&
    lhs.TurnCounter == rhs.TurnCounter &&
    lhs.winner == rhs.winner &&
    lhs.player == rhs.player;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::move_decision::Move_<ContainerAllocator1> & lhs, const ::move_decision::Move_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace move_decision

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::move_decision::Move_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::move_decision::Move_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::move_decision::Move_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::move_decision::Move_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::move_decision::Move_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::move_decision::Move_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::move_decision::Move_<ContainerAllocator> >
{
  static const char* value()
  {
    return "540f6692ebd5dddcb06a7ba689a29a28";
  }

  static const char* value(const ::move_decision::Move_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x540f6692ebd5dddcULL;
  static const uint64_t static_value2 = 0xb06a7ba689a29a28ULL;
};

template<class ContainerAllocator>
struct DataType< ::move_decision::Move_<ContainerAllocator> >
{
  static const char* value()
  {
    return "move_decision/Move";
  }

  static const char* value(const ::move_decision::Move_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::move_decision::Move_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int32 column\n"
"int32 TurnCounter\n"
"int32 winner\n"
"int32 player\n"
;
  }

  static const char* value(const ::move_decision::Move_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::move_decision::Move_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.column);
      stream.next(m.TurnCounter);
      stream.next(m.winner);
      stream.next(m.player);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct Move_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::move_decision::Move_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::move_decision::Move_<ContainerAllocator>& v)
  {
    s << indent << "column: ";
    Printer<int32_t>::stream(s, indent + "  ", v.column);
    s << indent << "TurnCounter: ";
    Printer<int32_t>::stream(s, indent + "  ", v.TurnCounter);
    s << indent << "winner: ";
    Printer<int32_t>::stream(s, indent + "  ", v.winner);
    s << indent << "player: ";
    Printer<int32_t>::stream(s, indent + "  ", v.player);
  }
};

} // namespace message_operations
} // namespace ros

#endif // MOVE_DECISION_MESSAGE_MOVE_H
