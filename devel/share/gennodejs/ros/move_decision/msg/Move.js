// Auto-generated. Do not edit!

// (in-package move_decision.msg)


"use strict";

const _serializer = _ros_msg_utils.Serialize;
const _arraySerializer = _serializer.Array;
const _deserializer = _ros_msg_utils.Deserialize;
const _arrayDeserializer = _deserializer.Array;
const _finder = _ros_msg_utils.Find;
const _getByteLength = _ros_msg_utils.getByteLength;

//-----------------------------------------------------------

class Move {
  constructor(initObj={}) {
    if (initObj === null) {
      // initObj === null is a special case for deserialization where we don't initialize fields
      this.column = null;
      this.TurnCounter = null;
      this.winner = null;
      this.player = null;
    }
    else {
      if (initObj.hasOwnProperty('column')) {
        this.column = initObj.column
      }
      else {
        this.column = 0;
      }
      if (initObj.hasOwnProperty('TurnCounter')) {
        this.TurnCounter = initObj.TurnCounter
      }
      else {
        this.TurnCounter = 0;
      }
      if (initObj.hasOwnProperty('winner')) {
        this.winner = initObj.winner
      }
      else {
        this.winner = 0;
      }
      if (initObj.hasOwnProperty('player')) {
        this.player = initObj.player
      }
      else {
        this.player = 0;
      }
    }
  }

  static serialize(obj, buffer, bufferOffset) {
    // Serializes a message object of type Move
    // Serialize message field [column]
    bufferOffset = _serializer.int32(obj.column, buffer, bufferOffset);
    // Serialize message field [TurnCounter]
    bufferOffset = _serializer.int32(obj.TurnCounter, buffer, bufferOffset);
    // Serialize message field [winner]
    bufferOffset = _serializer.int32(obj.winner, buffer, bufferOffset);
    // Serialize message field [player]
    bufferOffset = _serializer.int32(obj.player, buffer, bufferOffset);
    return bufferOffset;
  }

  static deserialize(buffer, bufferOffset=[0]) {
    //deserializes a message object of type Move
    let len;
    let data = new Move(null);
    // Deserialize message field [column]
    data.column = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [TurnCounter]
    data.TurnCounter = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [winner]
    data.winner = _deserializer.int32(buffer, bufferOffset);
    // Deserialize message field [player]
    data.player = _deserializer.int32(buffer, bufferOffset);
    return data;
  }

  static getMessageSize(object) {
    return 16;
  }

  static datatype() {
    // Returns string type for a message object
    return 'move_decision/Move';
  }

  static md5sum() {
    //Returns md5sum for a message object
    return '540f6692ebd5dddcb06a7ba689a29a28';
  }

  static messageDefinition() {
    // Returns full string definition for message
    return `
    int32 column
    int32 TurnCounter
    int32 winner
    int32 player
    
    `;
  }

  static Resolve(msg) {
    // deep-construct a valid message object instance of whatever was passed in
    if (typeof msg !== 'object' || msg === null) {
      msg = {};
    }
    const resolved = new Move(null);
    if (msg.column !== undefined) {
      resolved.column = msg.column;
    }
    else {
      resolved.column = 0
    }

    if (msg.TurnCounter !== undefined) {
      resolved.TurnCounter = msg.TurnCounter;
    }
    else {
      resolved.TurnCounter = 0
    }

    if (msg.winner !== undefined) {
      resolved.winner = msg.winner;
    }
    else {
      resolved.winner = 0
    }

    if (msg.player !== undefined) {
      resolved.player = msg.player;
    }
    else {
      resolved.player = 0
    }

    return resolved;
    }
};

module.exports = Move;
