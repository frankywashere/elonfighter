# Elon Fighter Game - Project Documentation

## Overview
This is a Street Fighter II-style fighting game featuring Elon Musk and Donald Trump as playable characters. The game is built using HTML5 Canvas and vanilla JavaScript.

## Main Game File
- **index.html** - The main game file (formerly fighter_enhanced.html)
- Uses HTML5 Canvas for rendering
- Includes mobile touch controls
- Features particle effects and advanced fighting mechanics

## Characters

### Elon (Player 1)
- Sprite folder: `elon/Elon1_normalized_v3/`
- Special moves:
  - **Flamethrower** (↓↘→ + Punch) - Uses `powermove-1.png` sprite, shoots flame particles
  - **Shoryuken** (→↓↘ + Punch) - Rising uppercut with invincibility frames  
  - **Tatsumaki** (↓↙← + Kick) - Spinning kick

### Trump (CPU/Player 2)
- Sprite folder: `trump1_normalized_v3/`
- Special moves:
  - **Money Throw** (↓↘→ + Punch) - Throws money bills with "HUSH MONEY!" text, uses `cash.png` sprite
  - **Shoryuken** (→↓↘ + Punch) - Rising uppercut with invincibility frames  
  - **Tatsumaki** (↓↙← + Kick) - Spinning kick

## Sprite System

### Normalization Script
- **normalize_sprites_v3.py** - Latest version of the sprite normalizer
- Uses Elon's standing height (728px) as reference
- Automatically crops sprites to remove transparent pixels
- Scales all sprites to consistent heights
- Creates standardized canvas sizes for smooth animations
- Run with: `python3 normalize_sprites_v3.py`

### Sprite Folders
- Original sprites: `elon/Elon1/` and `trump1/`
- Normalized sprites: `elon/Elon1_normalized_v3/` and `trump1_normalized_v3/`
- When adding new sprites:
  1. Add to original folder (e.g., `elon/Elon1/`)
  2. Run normalization script
  3. Update sprite mappings in index.html

## Game Controls

### Keyboard
- **Movement**: A/D (walk), S (crouch), W+A/D (jump)
- **Attacks**: 
  - Punch: U (light), I (medium), O (heavy)
  - Kick: J (light), K (medium), L (heavy)
- **Throw**: I+K (when close)
- **Block**: Hold back (A or D depending on facing)

### Special Move Inputs
- Quarter Circle Forward (↓↘→): 236
- Dragon Punch (→↓↘): 623  
- Quarter Circle Back (↓↙←): 214

## Recent Changes

### Character-Specific Projectiles (Latest)
1. **Elon's Flamethrower**:
   - Added `powermove-1.png` sprite showing "NOT-A-FLAMETHROWER"
   - Created `FlameParticle` class for flame effects
   - Multi-hit projectile (5 hits, 3 damage each)
   - Frame data: 10f startup, 35f active, 25f recovery
2. **Trump's Money Throw**:
   - Uses `cash.png` sprite for money bills
   - Created `MoneyBill` class with physics simulation
   - Multiple money bills spawn with "HUSH MONEY!" text effect
   - Uses `punch-standing.png` sprite for animation
   - Frame data: 20f duration, multi-hit capability
3. **Implementation**:
   - Modified `Projectile` class to check `owner.characterName`
   - Different behavior based on character (flamethrower vs money throw)
   - Created `TextEffect` class for special move text displays
   - Updated collision detection for multi-hit projectiles
   - Fixed sprite mapping so hadouken move uses 'powermove-1.png' for Elon
   - Updated both `drawCharacterSprite` and `getSpriteKey` methods to use correct sprite

## Technical Details

### Effects System
- Hit sparks: Yellow star burst on hit
- Block sparks: Blue square effect on block  
- Screen shake on heavy hits
- Global hit pause for impact feel
- Particle effects using Canvas 2D API

### Frame Data Structure
Each move has:
- startup: frames before hitbox appears
- active: frames hitbox is active
- recovery: frames after hitbox disappears
- damage, hitstun, blockstun, pushback
- Special properties: cancelable, invincible, knockdown, projectile

### Sprite Loading
Sprites are loaded via `SpriteManager` class with mappings defined in `spriteMappings` object. Each character has a base path and sprite filename mappings for each animation state.

## Git Repository
- Local repo: `/Users/frank/Desktop/elon game test/`
- NOT currently tracked in git (no .git folder)
- No GitHub remote set up yet

## Project Structure
```
elon game test/
├── index.html (main game)
├── fighter.html (old version - can be removed)
├── normalize_sprites_v3.py (sprite processor)
├── elon/
│   ├── Elon1/ (original sprites)
│   └── Elon1_normalized_v3/ (processed sprites)
├── trump1/
│   └── trump1_normalized_v3/ (processed sprites)
└── CLAUDE.md (this file)
```

## Notes for Future Sessions
- The main game file is now index.html (renamed from fighter_enhanced.html)
- Run sprite normalization after adding new sprites
- Check sprite mappings in HTML when adding new animations
- Flamethrower uses multi-hit collision with cooldown between hits
- Trump's money throw uses MoneyBill particles with physics simulation
- Text effects are implemented via TextEffect class for special moves
- Mobile controls are implemented but may need testing

---
Last Updated: 2025-08-01