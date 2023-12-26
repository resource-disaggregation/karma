/**
 * Autogenerated by Thrift Compiler (0.12.0)
 *
 * DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
 *  @generated
 */
package jiffy.directory;

@SuppressWarnings({"cast", "rawtypes", "serial", "unchecked", "unused"})
@javax.annotation.Generated(value = "Autogenerated by Thrift Compiler (0.12.0)")
public class rpc_data_status implements org.apache.thrift.TBase<rpc_data_status, rpc_data_status._Fields>, java.io.Serializable, Cloneable, Comparable<rpc_data_status> {
  private static final org.apache.thrift.protocol.TStruct STRUCT_DESC = new org.apache.thrift.protocol.TStruct("rpc_data_status");

  private static final org.apache.thrift.protocol.TField TYPE_FIELD_DESC = new org.apache.thrift.protocol.TField("type", org.apache.thrift.protocol.TType.STRING, (short)1);
  private static final org.apache.thrift.protocol.TField BACKING_PATH_FIELD_DESC = new org.apache.thrift.protocol.TField("backing_path", org.apache.thrift.protocol.TType.STRING, (short)2);
  private static final org.apache.thrift.protocol.TField CHAIN_LENGTH_FIELD_DESC = new org.apache.thrift.protocol.TField("chain_length", org.apache.thrift.protocol.TType.I32, (short)3);
  private static final org.apache.thrift.protocol.TField DATA_BLOCKS_FIELD_DESC = new org.apache.thrift.protocol.TField("data_blocks", org.apache.thrift.protocol.TType.LIST, (short)4);
  private static final org.apache.thrift.protocol.TField FLAGS_FIELD_DESC = new org.apache.thrift.protocol.TField("flags", org.apache.thrift.protocol.TType.I32, (short)5);
  private static final org.apache.thrift.protocol.TField TAGS_FIELD_DESC = new org.apache.thrift.protocol.TField("tags", org.apache.thrift.protocol.TType.MAP, (short)6);

  private static final org.apache.thrift.scheme.SchemeFactory STANDARD_SCHEME_FACTORY = new rpc_data_statusStandardSchemeFactory();
  private static final org.apache.thrift.scheme.SchemeFactory TUPLE_SCHEME_FACTORY = new rpc_data_statusTupleSchemeFactory();

  public @org.apache.thrift.annotation.Nullable java.lang.String type; // required
  public @org.apache.thrift.annotation.Nullable java.lang.String backing_path; // required
  public int chain_length; // required
  public @org.apache.thrift.annotation.Nullable java.util.List<rpc_replica_chain> data_blocks; // required
  public int flags; // required
  public @org.apache.thrift.annotation.Nullable java.util.Map<java.lang.String,java.lang.String> tags; // required

  /** The set of fields this struct contains, along with convenience methods for finding and manipulating them. */
  public enum _Fields implements org.apache.thrift.TFieldIdEnum {
    TYPE((short)1, "type"),
    BACKING_PATH((short)2, "backing_path"),
    CHAIN_LENGTH((short)3, "chain_length"),
    DATA_BLOCKS((short)4, "data_blocks"),
    FLAGS((short)5, "flags"),
    TAGS((short)6, "tags");

    private static final java.util.Map<java.lang.String, _Fields> byName = new java.util.HashMap<java.lang.String, _Fields>();

    static {
      for (_Fields field : java.util.EnumSet.allOf(_Fields.class)) {
        byName.put(field.getFieldName(), field);
      }
    }

    /**
     * Find the _Fields constant that matches fieldId, or null if its not found.
     */
    @org.apache.thrift.annotation.Nullable
    public static _Fields findByThriftId(int fieldId) {
      switch(fieldId) {
        case 1: // TYPE
          return TYPE;
        case 2: // BACKING_PATH
          return BACKING_PATH;
        case 3: // CHAIN_LENGTH
          return CHAIN_LENGTH;
        case 4: // DATA_BLOCKS
          return DATA_BLOCKS;
        case 5: // FLAGS
          return FLAGS;
        case 6: // TAGS
          return TAGS;
        default:
          return null;
      }
    }

    /**
     * Find the _Fields constant that matches fieldId, throwing an exception
     * if it is not found.
     */
    public static _Fields findByThriftIdOrThrow(int fieldId) {
      _Fields fields = findByThriftId(fieldId);
      if (fields == null) throw new java.lang.IllegalArgumentException("Field " + fieldId + " doesn't exist!");
      return fields;
    }

    /**
     * Find the _Fields constant that matches name, or null if its not found.
     */
    @org.apache.thrift.annotation.Nullable
    public static _Fields findByName(java.lang.String name) {
      return byName.get(name);
    }

    private final short _thriftId;
    private final java.lang.String _fieldName;

    _Fields(short thriftId, java.lang.String fieldName) {
      _thriftId = thriftId;
      _fieldName = fieldName;
    }

    public short getThriftFieldId() {
      return _thriftId;
    }

    public java.lang.String getFieldName() {
      return _fieldName;
    }
  }

  // isset id assignments
  private static final int __CHAIN_LENGTH_ISSET_ID = 0;
  private static final int __FLAGS_ISSET_ID = 1;
  private byte __isset_bitfield = 0;
  public static final java.util.Map<_Fields, org.apache.thrift.meta_data.FieldMetaData> metaDataMap;
  static {
    java.util.Map<_Fields, org.apache.thrift.meta_data.FieldMetaData> tmpMap = new java.util.EnumMap<_Fields, org.apache.thrift.meta_data.FieldMetaData>(_Fields.class);
    tmpMap.put(_Fields.TYPE, new org.apache.thrift.meta_data.FieldMetaData("type", org.apache.thrift.TFieldRequirementType.REQUIRED, 
        new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRING)));
    tmpMap.put(_Fields.BACKING_PATH, new org.apache.thrift.meta_data.FieldMetaData("backing_path", org.apache.thrift.TFieldRequirementType.REQUIRED, 
        new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRING)));
    tmpMap.put(_Fields.CHAIN_LENGTH, new org.apache.thrift.meta_data.FieldMetaData("chain_length", org.apache.thrift.TFieldRequirementType.REQUIRED, 
        new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.I32)));
    tmpMap.put(_Fields.DATA_BLOCKS, new org.apache.thrift.meta_data.FieldMetaData("data_blocks", org.apache.thrift.TFieldRequirementType.REQUIRED, 
        new org.apache.thrift.meta_data.ListMetaData(org.apache.thrift.protocol.TType.LIST, 
            new org.apache.thrift.meta_data.StructMetaData(org.apache.thrift.protocol.TType.STRUCT, rpc_replica_chain.class))));
    tmpMap.put(_Fields.FLAGS, new org.apache.thrift.meta_data.FieldMetaData("flags", org.apache.thrift.TFieldRequirementType.REQUIRED, 
        new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.I32)));
    tmpMap.put(_Fields.TAGS, new org.apache.thrift.meta_data.FieldMetaData("tags", org.apache.thrift.TFieldRequirementType.REQUIRED, 
        new org.apache.thrift.meta_data.MapMetaData(org.apache.thrift.protocol.TType.MAP, 
            new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRING), 
            new org.apache.thrift.meta_data.FieldValueMetaData(org.apache.thrift.protocol.TType.STRING))));
    metaDataMap = java.util.Collections.unmodifiableMap(tmpMap);
    org.apache.thrift.meta_data.FieldMetaData.addStructMetaDataMap(rpc_data_status.class, metaDataMap);
  }

  public rpc_data_status() {
  }

  public rpc_data_status(
    java.lang.String type,
    java.lang.String backing_path,
    int chain_length,
    java.util.List<rpc_replica_chain> data_blocks,
    int flags,
    java.util.Map<java.lang.String,java.lang.String> tags)
  {
    this();
    this.type = type;
    this.backing_path = backing_path;
    this.chain_length = chain_length;
    setChainLengthIsSet(true);
    this.data_blocks = data_blocks;
    this.flags = flags;
    setFlagsIsSet(true);
    this.tags = tags;
  }

  /**
   * Performs a deep copy on <i>other</i>.
   */
  public rpc_data_status(rpc_data_status other) {
    __isset_bitfield = other.__isset_bitfield;
    if (other.isSetType()) {
      this.type = other.type;
    }
    if (other.isSetBackingPath()) {
      this.backing_path = other.backing_path;
    }
    this.chain_length = other.chain_length;
    if (other.isSetDataBlocks()) {
      java.util.List<rpc_replica_chain> __this__data_blocks = new java.util.ArrayList<rpc_replica_chain>(other.data_blocks.size());
      for (rpc_replica_chain other_element : other.data_blocks) {
        __this__data_blocks.add(new rpc_replica_chain(other_element));
      }
      this.data_blocks = __this__data_blocks;
    }
    this.flags = other.flags;
    if (other.isSetTags()) {
      java.util.Map<java.lang.String,java.lang.String> __this__tags = new java.util.HashMap<java.lang.String,java.lang.String>(other.tags);
      this.tags = __this__tags;
    }
  }

  public rpc_data_status deepCopy() {
    return new rpc_data_status(this);
  }

  @Override
  public void clear() {
    this.type = null;
    this.backing_path = null;
    setChainLengthIsSet(false);
    this.chain_length = 0;
    if (this.data_blocks != null) {
      this.data_blocks.clear();
    }
    setFlagsIsSet(false);
    this.flags = 0;
    if (this.tags != null) {
      this.tags.clear();
    }
  }

  @org.apache.thrift.annotation.Nullable
  public java.lang.String getType() {
    return this.type;
  }

  public rpc_data_status setType(@org.apache.thrift.annotation.Nullable java.lang.String type) {
    this.type = type;
    return this;
  }

  public void unsetType() {
    this.type = null;
  }

  /** Returns true if field type is set (has been assigned a value) and false otherwise */
  public boolean isSetType() {
    return this.type != null;
  }

  public void setTypeIsSet(boolean value) {
    if (!value) {
      this.type = null;
    }
  }

  @org.apache.thrift.annotation.Nullable
  public java.lang.String getBackingPath() {
    return this.backing_path;
  }

  public rpc_data_status setBackingPath(@org.apache.thrift.annotation.Nullable java.lang.String backing_path) {
    this.backing_path = backing_path;
    return this;
  }

  public void unsetBackingPath() {
    this.backing_path = null;
  }

  /** Returns true if field backing_path is set (has been assigned a value) and false otherwise */
  public boolean isSetBackingPath() {
    return this.backing_path != null;
  }

  public void setBackingPathIsSet(boolean value) {
    if (!value) {
      this.backing_path = null;
    }
  }

  public int getChainLength() {
    return this.chain_length;
  }

  public rpc_data_status setChainLength(int chain_length) {
    this.chain_length = chain_length;
    setChainLengthIsSet(true);
    return this;
  }

  public void unsetChainLength() {
    __isset_bitfield = org.apache.thrift.EncodingUtils.clearBit(__isset_bitfield, __CHAIN_LENGTH_ISSET_ID);
  }

  /** Returns true if field chain_length is set (has been assigned a value) and false otherwise */
  public boolean isSetChainLength() {
    return org.apache.thrift.EncodingUtils.testBit(__isset_bitfield, __CHAIN_LENGTH_ISSET_ID);
  }

  public void setChainLengthIsSet(boolean value) {
    __isset_bitfield = org.apache.thrift.EncodingUtils.setBit(__isset_bitfield, __CHAIN_LENGTH_ISSET_ID, value);
  }

  public int getDataBlocksSize() {
    return (this.data_blocks == null) ? 0 : this.data_blocks.size();
  }

  @org.apache.thrift.annotation.Nullable
  public java.util.Iterator<rpc_replica_chain> getDataBlocksIterator() {
    return (this.data_blocks == null) ? null : this.data_blocks.iterator();
  }

  public void addToDataBlocks(rpc_replica_chain elem) {
    if (this.data_blocks == null) {
      this.data_blocks = new java.util.ArrayList<rpc_replica_chain>();
    }
    this.data_blocks.add(elem);
  }

  @org.apache.thrift.annotation.Nullable
  public java.util.List<rpc_replica_chain> getDataBlocks() {
    return this.data_blocks;
  }

  public rpc_data_status setDataBlocks(@org.apache.thrift.annotation.Nullable java.util.List<rpc_replica_chain> data_blocks) {
    this.data_blocks = data_blocks;
    return this;
  }

  public void unsetDataBlocks() {
    this.data_blocks = null;
  }

  /** Returns true if field data_blocks is set (has been assigned a value) and false otherwise */
  public boolean isSetDataBlocks() {
    return this.data_blocks != null;
  }

  public void setDataBlocksIsSet(boolean value) {
    if (!value) {
      this.data_blocks = null;
    }
  }

  public int getFlags() {
    return this.flags;
  }

  public rpc_data_status setFlags(int flags) {
    this.flags = flags;
    setFlagsIsSet(true);
    return this;
  }

  public void unsetFlags() {
    __isset_bitfield = org.apache.thrift.EncodingUtils.clearBit(__isset_bitfield, __FLAGS_ISSET_ID);
  }

  /** Returns true if field flags is set (has been assigned a value) and false otherwise */
  public boolean isSetFlags() {
    return org.apache.thrift.EncodingUtils.testBit(__isset_bitfield, __FLAGS_ISSET_ID);
  }

  public void setFlagsIsSet(boolean value) {
    __isset_bitfield = org.apache.thrift.EncodingUtils.setBit(__isset_bitfield, __FLAGS_ISSET_ID, value);
  }

  public int getTagsSize() {
    return (this.tags == null) ? 0 : this.tags.size();
  }

  public void putToTags(java.lang.String key, java.lang.String val) {
    if (this.tags == null) {
      this.tags = new java.util.HashMap<java.lang.String,java.lang.String>();
    }
    this.tags.put(key, val);
  }

  @org.apache.thrift.annotation.Nullable
  public java.util.Map<java.lang.String,java.lang.String> getTags() {
    return this.tags;
  }

  public rpc_data_status setTags(@org.apache.thrift.annotation.Nullable java.util.Map<java.lang.String,java.lang.String> tags) {
    this.tags = tags;
    return this;
  }

  public void unsetTags() {
    this.tags = null;
  }

  /** Returns true if field tags is set (has been assigned a value) and false otherwise */
  public boolean isSetTags() {
    return this.tags != null;
  }

  public void setTagsIsSet(boolean value) {
    if (!value) {
      this.tags = null;
    }
  }

  public void setFieldValue(_Fields field, @org.apache.thrift.annotation.Nullable java.lang.Object value) {
    switch (field) {
    case TYPE:
      if (value == null) {
        unsetType();
      } else {
        setType((java.lang.String)value);
      }
      break;

    case BACKING_PATH:
      if (value == null) {
        unsetBackingPath();
      } else {
        setBackingPath((java.lang.String)value);
      }
      break;

    case CHAIN_LENGTH:
      if (value == null) {
        unsetChainLength();
      } else {
        setChainLength((java.lang.Integer)value);
      }
      break;

    case DATA_BLOCKS:
      if (value == null) {
        unsetDataBlocks();
      } else {
        setDataBlocks((java.util.List<rpc_replica_chain>)value);
      }
      break;

    case FLAGS:
      if (value == null) {
        unsetFlags();
      } else {
        setFlags((java.lang.Integer)value);
      }
      break;

    case TAGS:
      if (value == null) {
        unsetTags();
      } else {
        setTags((java.util.Map<java.lang.String,java.lang.String>)value);
      }
      break;

    }
  }

  @org.apache.thrift.annotation.Nullable
  public java.lang.Object getFieldValue(_Fields field) {
    switch (field) {
    case TYPE:
      return getType();

    case BACKING_PATH:
      return getBackingPath();

    case CHAIN_LENGTH:
      return getChainLength();

    case DATA_BLOCKS:
      return getDataBlocks();

    case FLAGS:
      return getFlags();

    case TAGS:
      return getTags();

    }
    throw new java.lang.IllegalStateException();
  }

  /** Returns true if field corresponding to fieldID is set (has been assigned a value) and false otherwise */
  public boolean isSet(_Fields field) {
    if (field == null) {
      throw new java.lang.IllegalArgumentException();
    }

    switch (field) {
    case TYPE:
      return isSetType();
    case BACKING_PATH:
      return isSetBackingPath();
    case CHAIN_LENGTH:
      return isSetChainLength();
    case DATA_BLOCKS:
      return isSetDataBlocks();
    case FLAGS:
      return isSetFlags();
    case TAGS:
      return isSetTags();
    }
    throw new java.lang.IllegalStateException();
  }

  @Override
  public boolean equals(java.lang.Object that) {
    if (that == null)
      return false;
    if (that instanceof rpc_data_status)
      return this.equals((rpc_data_status)that);
    return false;
  }

  public boolean equals(rpc_data_status that) {
    if (that == null)
      return false;
    if (this == that)
      return true;

    boolean this_present_type = true && this.isSetType();
    boolean that_present_type = true && that.isSetType();
    if (this_present_type || that_present_type) {
      if (!(this_present_type && that_present_type))
        return false;
      if (!this.type.equals(that.type))
        return false;
    }

    boolean this_present_backing_path = true && this.isSetBackingPath();
    boolean that_present_backing_path = true && that.isSetBackingPath();
    if (this_present_backing_path || that_present_backing_path) {
      if (!(this_present_backing_path && that_present_backing_path))
        return false;
      if (!this.backing_path.equals(that.backing_path))
        return false;
    }

    boolean this_present_chain_length = true;
    boolean that_present_chain_length = true;
    if (this_present_chain_length || that_present_chain_length) {
      if (!(this_present_chain_length && that_present_chain_length))
        return false;
      if (this.chain_length != that.chain_length)
        return false;
    }

    boolean this_present_data_blocks = true && this.isSetDataBlocks();
    boolean that_present_data_blocks = true && that.isSetDataBlocks();
    if (this_present_data_blocks || that_present_data_blocks) {
      if (!(this_present_data_blocks && that_present_data_blocks))
        return false;
      if (!this.data_blocks.equals(that.data_blocks))
        return false;
    }

    boolean this_present_flags = true;
    boolean that_present_flags = true;
    if (this_present_flags || that_present_flags) {
      if (!(this_present_flags && that_present_flags))
        return false;
      if (this.flags != that.flags)
        return false;
    }

    boolean this_present_tags = true && this.isSetTags();
    boolean that_present_tags = true && that.isSetTags();
    if (this_present_tags || that_present_tags) {
      if (!(this_present_tags && that_present_tags))
        return false;
      if (!this.tags.equals(that.tags))
        return false;
    }

    return true;
  }

  @Override
  public int hashCode() {
    int hashCode = 1;

    hashCode = hashCode * 8191 + ((isSetType()) ? 131071 : 524287);
    if (isSetType())
      hashCode = hashCode * 8191 + type.hashCode();

    hashCode = hashCode * 8191 + ((isSetBackingPath()) ? 131071 : 524287);
    if (isSetBackingPath())
      hashCode = hashCode * 8191 + backing_path.hashCode();

    hashCode = hashCode * 8191 + chain_length;

    hashCode = hashCode * 8191 + ((isSetDataBlocks()) ? 131071 : 524287);
    if (isSetDataBlocks())
      hashCode = hashCode * 8191 + data_blocks.hashCode();

    hashCode = hashCode * 8191 + flags;

    hashCode = hashCode * 8191 + ((isSetTags()) ? 131071 : 524287);
    if (isSetTags())
      hashCode = hashCode * 8191 + tags.hashCode();

    return hashCode;
  }

  @Override
  public int compareTo(rpc_data_status other) {
    if (!getClass().equals(other.getClass())) {
      return getClass().getName().compareTo(other.getClass().getName());
    }

    int lastComparison = 0;

    lastComparison = java.lang.Boolean.valueOf(isSetType()).compareTo(other.isSetType());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetType()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.type, other.type);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    lastComparison = java.lang.Boolean.valueOf(isSetBackingPath()).compareTo(other.isSetBackingPath());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetBackingPath()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.backing_path, other.backing_path);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    lastComparison = java.lang.Boolean.valueOf(isSetChainLength()).compareTo(other.isSetChainLength());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetChainLength()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.chain_length, other.chain_length);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    lastComparison = java.lang.Boolean.valueOf(isSetDataBlocks()).compareTo(other.isSetDataBlocks());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetDataBlocks()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.data_blocks, other.data_blocks);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    lastComparison = java.lang.Boolean.valueOf(isSetFlags()).compareTo(other.isSetFlags());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetFlags()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.flags, other.flags);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    lastComparison = java.lang.Boolean.valueOf(isSetTags()).compareTo(other.isSetTags());
    if (lastComparison != 0) {
      return lastComparison;
    }
    if (isSetTags()) {
      lastComparison = org.apache.thrift.TBaseHelper.compareTo(this.tags, other.tags);
      if (lastComparison != 0) {
        return lastComparison;
      }
    }
    return 0;
  }

  @org.apache.thrift.annotation.Nullable
  public _Fields fieldForId(int fieldId) {
    return _Fields.findByThriftId(fieldId);
  }

  public void read(org.apache.thrift.protocol.TProtocol iprot) throws org.apache.thrift.TException {
    scheme(iprot).read(iprot, this);
  }

  public void write(org.apache.thrift.protocol.TProtocol oprot) throws org.apache.thrift.TException {
    scheme(oprot).write(oprot, this);
  }

  @Override
  public java.lang.String toString() {
    java.lang.StringBuilder sb = new java.lang.StringBuilder("rpc_data_status(");
    boolean first = true;

    sb.append("type:");
    if (this.type == null) {
      sb.append("null");
    } else {
      sb.append(this.type);
    }
    first = false;
    if (!first) sb.append(", ");
    sb.append("backing_path:");
    if (this.backing_path == null) {
      sb.append("null");
    } else {
      sb.append(this.backing_path);
    }
    first = false;
    if (!first) sb.append(", ");
    sb.append("chain_length:");
    sb.append(this.chain_length);
    first = false;
    if (!first) sb.append(", ");
    sb.append("data_blocks:");
    if (this.data_blocks == null) {
      sb.append("null");
    } else {
      sb.append(this.data_blocks);
    }
    first = false;
    if (!first) sb.append(", ");
    sb.append("flags:");
    sb.append(this.flags);
    first = false;
    if (!first) sb.append(", ");
    sb.append("tags:");
    if (this.tags == null) {
      sb.append("null");
    } else {
      sb.append(this.tags);
    }
    first = false;
    sb.append(")");
    return sb.toString();
  }

  public void validate() throws org.apache.thrift.TException {
    // check for required fields
    if (type == null) {
      throw new org.apache.thrift.protocol.TProtocolException("Required field 'type' was not present! Struct: " + toString());
    }
    if (backing_path == null) {
      throw new org.apache.thrift.protocol.TProtocolException("Required field 'backing_path' was not present! Struct: " + toString());
    }
    // alas, we cannot check 'chain_length' because it's a primitive and you chose the non-beans generator.
    if (data_blocks == null) {
      throw new org.apache.thrift.protocol.TProtocolException("Required field 'data_blocks' was not present! Struct: " + toString());
    }
    // alas, we cannot check 'flags' because it's a primitive and you chose the non-beans generator.
    if (tags == null) {
      throw new org.apache.thrift.protocol.TProtocolException("Required field 'tags' was not present! Struct: " + toString());
    }
    // check for sub-struct validity
  }

  private void writeObject(java.io.ObjectOutputStream out) throws java.io.IOException {
    try {
      write(new org.apache.thrift.protocol.TCompactProtocol(new org.apache.thrift.transport.TIOStreamTransport(out)));
    } catch (org.apache.thrift.TException te) {
      throw new java.io.IOException(te);
    }
  }

  private void readObject(java.io.ObjectInputStream in) throws java.io.IOException, java.lang.ClassNotFoundException {
    try {
      // it doesn't seem like you should have to do this, but java serialization is wacky, and doesn't call the default constructor.
      __isset_bitfield = 0;
      read(new org.apache.thrift.protocol.TCompactProtocol(new org.apache.thrift.transport.TIOStreamTransport(in)));
    } catch (org.apache.thrift.TException te) {
      throw new java.io.IOException(te);
    }
  }

  private static class rpc_data_statusStandardSchemeFactory implements org.apache.thrift.scheme.SchemeFactory {
    public rpc_data_statusStandardScheme getScheme() {
      return new rpc_data_statusStandardScheme();
    }
  }

  private static class rpc_data_statusStandardScheme extends org.apache.thrift.scheme.StandardScheme<rpc_data_status> {

    public void read(org.apache.thrift.protocol.TProtocol iprot, rpc_data_status struct) throws org.apache.thrift.TException {
      org.apache.thrift.protocol.TField schemeField;
      iprot.readStructBegin();
      while (true)
      {
        schemeField = iprot.readFieldBegin();
        if (schemeField.type == org.apache.thrift.protocol.TType.STOP) { 
          break;
        }
        switch (schemeField.id) {
          case 1: // TYPE
            if (schemeField.type == org.apache.thrift.protocol.TType.STRING) {
              struct.type = iprot.readString();
              struct.setTypeIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          case 2: // BACKING_PATH
            if (schemeField.type == org.apache.thrift.protocol.TType.STRING) {
              struct.backing_path = iprot.readString();
              struct.setBackingPathIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          case 3: // CHAIN_LENGTH
            if (schemeField.type == org.apache.thrift.protocol.TType.I32) {
              struct.chain_length = iprot.readI32();
              struct.setChainLengthIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          case 4: // DATA_BLOCKS
            if (schemeField.type == org.apache.thrift.protocol.TType.LIST) {
              {
                org.apache.thrift.protocol.TList _list8 = iprot.readListBegin();
                if (struct.data_blocks == null) {
                  struct.data_blocks = new java.util.ArrayList<rpc_replica_chain>(_list8.size);
                }
                @org.apache.thrift.annotation.Nullable rpc_replica_chain _elem9 = new rpc_replica_chain();
                for (int _i10 = 0; _i10 < _list8.size; ++_i10)
                {
                  if (_elem9 == null) {
                    _elem9 = new rpc_replica_chain();
                  }
                  _elem9.read(iprot);
                  struct.data_blocks.add(_elem9);
                  _elem9 = null;
                }
                iprot.readListEnd();
              }
              struct.setDataBlocksIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          case 5: // FLAGS
            if (schemeField.type == org.apache.thrift.protocol.TType.I32) {
              struct.flags = iprot.readI32();
              struct.setFlagsIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          case 6: // TAGS
            if (schemeField.type == org.apache.thrift.protocol.TType.MAP) {
              {
                org.apache.thrift.protocol.TMap _map11 = iprot.readMapBegin();
                if (struct.tags == null) {
                  struct.tags = new java.util.HashMap<java.lang.String,java.lang.String>(2*_map11.size);
                }
                @org.apache.thrift.annotation.Nullable java.lang.String _key12 = null;
                @org.apache.thrift.annotation.Nullable java.lang.String _val13 = null;
                for (int _i14 = 0; _i14 < _map11.size; ++_i14)
                {
                  _key12 = iprot.readString();
                  _val13 = iprot.readString();
                  struct.tags.put(_key12, _val13);
                }
                iprot.readMapEnd();
              }
              struct.setTagsIsSet(true);
            } else { 
              org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
            }
            break;
          default:
            org.apache.thrift.protocol.TProtocolUtil.skip(iprot, schemeField.type);
        }
        iprot.readFieldEnd();
      }
      iprot.readStructEnd();

      // check for required fields of primitive type, which can't be checked in the validate method
      if (!struct.isSetChainLength()) {
        throw new org.apache.thrift.protocol.TProtocolException("Required field 'chain_length' was not found in serialized data! Struct: " + toString());
      }
      if (!struct.isSetFlags()) {
        throw new org.apache.thrift.protocol.TProtocolException("Required field 'flags' was not found in serialized data! Struct: " + toString());
      }
      struct.validate();
    }

    public void write(org.apache.thrift.protocol.TProtocol oprot, rpc_data_status struct) throws org.apache.thrift.TException {
      struct.validate();

      oprot.writeStructBegin(STRUCT_DESC);
      if (struct.type != null) {
        oprot.writeFieldBegin(TYPE_FIELD_DESC);
        oprot.writeString(struct.type);
        oprot.writeFieldEnd();
      }
      if (struct.backing_path != null) {
        oprot.writeFieldBegin(BACKING_PATH_FIELD_DESC);
        oprot.writeString(struct.backing_path);
        oprot.writeFieldEnd();
      }
      oprot.writeFieldBegin(CHAIN_LENGTH_FIELD_DESC);
      oprot.writeI32(struct.chain_length);
      oprot.writeFieldEnd();
      if (struct.data_blocks != null) {
        oprot.writeFieldBegin(DATA_BLOCKS_FIELD_DESC);
        {
          oprot.writeListBegin(new org.apache.thrift.protocol.TList(org.apache.thrift.protocol.TType.STRUCT, struct.data_blocks.size()));
          for (rpc_replica_chain _iter15 : struct.data_blocks)
          {
            _iter15.write(oprot);
          }
          oprot.writeListEnd();
        }
        oprot.writeFieldEnd();
      }
      oprot.writeFieldBegin(FLAGS_FIELD_DESC);
      oprot.writeI32(struct.flags);
      oprot.writeFieldEnd();
      if (struct.tags != null) {
        oprot.writeFieldBegin(TAGS_FIELD_DESC);
        {
          oprot.writeMapBegin(new org.apache.thrift.protocol.TMap(org.apache.thrift.protocol.TType.STRING, org.apache.thrift.protocol.TType.STRING, struct.tags.size()));
          for (java.util.Map.Entry<java.lang.String, java.lang.String> _iter16 : struct.tags.entrySet())
          {
            oprot.writeString(_iter16.getKey());
            oprot.writeString(_iter16.getValue());
          }
          oprot.writeMapEnd();
        }
        oprot.writeFieldEnd();
      }
      oprot.writeFieldStop();
      oprot.writeStructEnd();
    }

  }

  private static class rpc_data_statusTupleSchemeFactory implements org.apache.thrift.scheme.SchemeFactory {
    public rpc_data_statusTupleScheme getScheme() {
      return new rpc_data_statusTupleScheme();
    }
  }

  private static class rpc_data_statusTupleScheme extends org.apache.thrift.scheme.TupleScheme<rpc_data_status> {

    @Override
    public void write(org.apache.thrift.protocol.TProtocol prot, rpc_data_status struct) throws org.apache.thrift.TException {
      org.apache.thrift.protocol.TTupleProtocol oprot = (org.apache.thrift.protocol.TTupleProtocol) prot;
      oprot.writeString(struct.type);
      oprot.writeString(struct.backing_path);
      oprot.writeI32(struct.chain_length);
      {
        oprot.writeI32(struct.data_blocks.size());
        for (rpc_replica_chain _iter17 : struct.data_blocks)
        {
          _iter17.write(oprot);
        }
      }
      oprot.writeI32(struct.flags);
      {
        oprot.writeI32(struct.tags.size());
        for (java.util.Map.Entry<java.lang.String, java.lang.String> _iter18 : struct.tags.entrySet())
        {
          oprot.writeString(_iter18.getKey());
          oprot.writeString(_iter18.getValue());
        }
      }
    }

    @Override
    public void read(org.apache.thrift.protocol.TProtocol prot, rpc_data_status struct) throws org.apache.thrift.TException {
      org.apache.thrift.protocol.TTupleProtocol iprot = (org.apache.thrift.protocol.TTupleProtocol) prot;
      struct.type = iprot.readString();
      struct.setTypeIsSet(true);
      struct.backing_path = iprot.readString();
      struct.setBackingPathIsSet(true);
      struct.chain_length = iprot.readI32();
      struct.setChainLengthIsSet(true);
      {
        org.apache.thrift.protocol.TList _list19 = new org.apache.thrift.protocol.TList(org.apache.thrift.protocol.TType.STRUCT, iprot.readI32());
        if (struct.data_blocks == null) {
          struct.data_blocks = new java.util.ArrayList<rpc_replica_chain>(_list19.size);
        }
        @org.apache.thrift.annotation.Nullable rpc_replica_chain _elem20 = new rpc_replica_chain();
        for (int _i21 = 0; _i21 < _list19.size; ++_i21)
        {
          if (_elem20 == null) {
            _elem20 = new rpc_replica_chain();
          }
          _elem20.read(iprot);
          struct.data_blocks.add(_elem20);
          _elem20 = null;
        }
      }
      struct.setDataBlocksIsSet(true);
      struct.flags = iprot.readI32();
      struct.setFlagsIsSet(true);
      {
        org.apache.thrift.protocol.TMap _map22 = new org.apache.thrift.protocol.TMap(org.apache.thrift.protocol.TType.STRING, org.apache.thrift.protocol.TType.STRING, iprot.readI32());
        if (struct.tags == null) {
          struct.tags = new java.util.HashMap<java.lang.String,java.lang.String>(2*_map22.size);
        }
        @org.apache.thrift.annotation.Nullable java.lang.String _key23 = null;
        @org.apache.thrift.annotation.Nullable java.lang.String _val24 = null;
        for (int _i25 = 0; _i25 < _map22.size; ++_i25)
        {
          _key23 = iprot.readString();
          _val24 = iprot.readString();
          struct.tags.put(_key23, _val24);
        }
      }
      struct.setTagsIsSet(true);
    }
  }

  private static <S extends org.apache.thrift.scheme.IScheme> S scheme(org.apache.thrift.protocol.TProtocol proto) {
    return (org.apache.thrift.scheme.StandardScheme.class.equals(proto.getScheme()) ? STANDARD_SCHEME_FACTORY : TUPLE_SCHEME_FACTORY).getScheme();
  }
}
