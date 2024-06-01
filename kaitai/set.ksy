meta:
  id: set_file
  file-extension: set
  endian: le

seq:
  - id: header
    type: header
    if: is_file
    
  - id: num_enemies
    type: u4
    
  - id: header2
    size: "is_file ? 60 : 20"
    
  - id: enemies
    type: enemy
    repeat: expr
    repeat-expr: num_enemies

params:
  - id: is_file
    type: bool

enums:
  enemy_state:
    0: inactive
    0x3F80: active

types:
  header:
    seq:
      - id: magic
        contents: "OSE"
        
      - id: unused
        size: 5
        
      - id: file_size
        type: u4

  enemy:
    seq:
      - id: pad1
        size: 4
        
      - id: angle
        type: f4
        
      - id: pad2
        size: 2
        # valid:
        #   any-of: ["[0, 0]", "[81, 169]", "[180, 194]", "[156, 66]"]
        
      - id: unknown1
        size: 2
        
      - id: pad3
        size: 4
        valid:
          any-of: ["[0, 0, 0, 0]"]
        
      - id: x
        type: f4
        
      - id: y
        type: f4
        
      - id: z
        type: f4
      
      - id: pad4
        size: 2
        valid: "[0, 0]"
        
      - id: state
        type: u2
        enum: enemy_state
      
      - id: category
        size: 4
        
      - id: pad5
        size: 4
        
      - id: enemy_type
        size: 8
        type: str
        encoding: UTF-8
        terminator: 0
        
      - id: pad6
        size: 30
        
      - id: pad7
        size: 2
        valid: "[178, 253]"