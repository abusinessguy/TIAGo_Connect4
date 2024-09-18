// Generated by gencpp from file action_server/MoveToPoseResult.msg
// DO NOT EDIT!


#ifndef ACTION_SERVER_MESSAGE_MOVETOPOSERESULT_H
#define ACTION_SERVER_MESSAGE_MOVETOPOSERESULT_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace action_server
{
template <class ContainerAllocator>
struct MoveToPoseResult_
{
  typedef MoveToPoseResult_<ContainerAllocator> Type;

  MoveToPoseResult_()
    : success(false)  {
    }
  MoveToPoseResult_(const ContainerAllocator& _alloc)
    : success(false)  {
  (void)_alloc;
    }



   typedef uint8_t _success_type;
  _success_type success;





  typedef boost::shared_ptr< ::action_server::MoveToPoseResult_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::action_server::MoveToPoseResult_<ContainerAllocator> const> ConstPtr;

}; // struct MoveToPoseResult_

typedef ::action_server::MoveToPoseResult_<std::allocator<void> > MoveToPoseResult;

typedef boost::shared_ptr< ::action_server::MoveToPoseResult > MoveToPoseResultPtr;
typedef boost::shared_ptr< ::action_server::MoveToPoseResult const> MoveToPoseResultConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::action_server::MoveToPoseResult_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::action_server::MoveToPoseResult_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::action_server::MoveToPoseResult_<ContainerAllocator1> & lhs, const ::action_server::MoveToPoseResult_<ContainerAllocator2> & rhs)
{
  return lhs.success == rhs.success;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::action_server::MoveToPoseResult_<ContainerAllocator1> & lhs, const ::action_server::MoveToPoseResult_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace action_server

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::action_server::MoveToPoseResult_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::action_server::MoveToPoseResult_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::action_server::MoveToPoseResult_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::action_server::MoveToPoseResult_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::action_server::MoveToPoseResult_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::action_server::MoveToPoseResult_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::action_server::MoveToPoseResult_<ContainerAllocator> >
{
  static const char* value()
  {
    return "358e233cde0c8a8bcfea4ce193f8fc15";
  }

  static const char* value(const ::action_server::MoveToPoseResult_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x358e233cde0c8a8bULL;
  static const uint64_t static_value2 = 0xcfea4ce193f8fc15ULL;
};

template<class ContainerAllocator>
struct DataType< ::action_server::MoveToPoseResult_<ContainerAllocator> >
{
  static const char* value()
  {
    return "action_server/MoveToPoseResult";
  }

  static const char* value(const ::action_server::MoveToPoseResult_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::action_server::MoveToPoseResult_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"# Result (optional)\n"
"bool success\n"
"\n"
;
  }

  static const char* value(const ::action_server::MoveToPoseResult_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::action_server::MoveToPoseResult_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.success);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct MoveToPoseResult_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::action_server::MoveToPoseResult_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::action_server::MoveToPoseResult_<ContainerAllocator>& v)
  {
    s << indent << "success: ";
    Printer<uint8_t>::stream(s, indent + "  ", v.success);
  }
};

} // namespace message_operations
} // namespace ros

#endif // ACTION_SERVER_MESSAGE_MOVETOPOSERESULT_H
