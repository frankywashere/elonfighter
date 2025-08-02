# Elon Fighter Game - Project Documentation

## IMPORTANT: Keep This File Updated!
**This file must be updated whenever ANY changes are made to the game. This ensures future sessions have accurate information about the project state.**

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
  - **Throw** (I+K when close) - Uses `throw.png` sprite (scaled down 20% with scale_throw_sprite.py)

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

### Ghost Trail System (2025-08-02 - Latest)
- **Ghost Trail Manager**: Implemented visual trail effects for special moves
  - Disabled by default, toggle with 'G' key
  - Per-move configuration (shoryuken, tatsumaki, dash, etc.)
  - Color-coded trails: Green for Elon, Red for Trump
  - Configurable opacity, fade speed, and interval per move
  - Only activates during specific moves or high-speed movements
- **Technical Implementation**:
  - `GhostTrailManager` class manages trail creation and rendering
  - Stores fighter state snapshots (position, sprite, animation frame)
  - Uses screen blend mode for ethereal effect
  - Integrated into game loop for automatic updates

### Walk Cycle and Mobile Button Fix (2025-08-02)
- **Elon Walk Cycle Update**: Changed from 3-frame cycle (0-1-2) to 4-step cycle (0-1-2-1-0)
  - Creates smoother walking animation with return motion
  - Uses frames: walking1.png → walking2.png → walking3.png → walking2.png → repeat
  - **Frame Duration**: Increased from 6 to 20 frames per step for much slower transitions
- **Mobile Restart Button Fix**: Fixed click event being blocked by preventDefault
  - Added exception for restart button in touch event handler
  - Button now properly reloads page when clicked

### Mobile Restart Button (2025-08-02)
- Added restart button for mobile devices that appears after game over
- CSS styling with red background and retro game aesthetic
- Shows only on mobile devices when game ends
- Reloads page on click to start new game

### Throw Animation Fixes (2025-08-02)
1. **Throw Sprite Added**:
   - Added `throw.png` sprite for Elon's throw animation
   - Scaled down 20% using `scale_throw_sprite.py` for better proportions
   - Backup created as `throw_backup.png`
2. **Rotation Removed**:
   - Removed rotation animation when characters are thrown
   - Characters now stay upright during throw animation
   - Cleaner visual appearance

### Blocking Bug Fixes (2025-08-02)
1. **Movement Restriction Fix**:
   - Fixed bug where player could get stuck unable to move backwards
   - Removed overly restrictive `veryClose` condition in blocking logic
   - Improved blocking to only activate during actual threats
2. **AI Toggle Fix**:
   - Added proper state reset when toggling AI with '1' key
   - Prevents AI from getting stuck in attack state

### Character-Specific Projectiles
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
- Ghost trails: Visual afterimage effects for special moves

### Ghost Trail System
- **GhostTrailManager**: Controls afterimage effects
  - Default state: Disabled (toggle with 'G' key)
  - Per-move configuration in `trailConfig` object
  - Properties per move: enabled, interval, opacity, fadeSpeed
  - Color coding: Green trails for Elon, red for Trump
- **Supported Moves**:
  - Shoryuken: High opacity, slow fade
  - Tatsumaki: Medium opacity, moderate fade
  - Dash movements: Lower opacity, fast fade
  - Jump kicks and heavy punches: Configurable per move
- **Rendering**: Uses screen blend mode with character sprites

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
- GitHub remote: `https://github.com/frankywashere/elonfighter.git`
- Main branch: `main`
- Other branches: `gh-pages`, `webgl-motion-blur`

## Project Structure
```
elon game test/
├── index.html (main game)
├── fighter.html (old version - can be removed)
├── normalize_sprites_v3.py (sprite processor)
├── scale_throw_sprite.py (utility to scale throw sprite)
├── elon/
│   ├── Elon1/ (original sprites)
│   └── Elon1_normalized_v3/ (processed sprites)
├── trump1/
│   └── trump1_normalized_v3/ (processed sprites)
└── CLAUDE.md (this file - MUST BE KEPT UPDATED!)
```

## Notes for Future Sessions
- **ALWAYS UPDATE THIS FILE** when making changes to the game
- The main game file is now index.html (renamed from fighter_enhanced.html)
- Run sprite normalization after adding new sprites
- Check sprite mappings in HTML when adding new animations
- Flamethrower uses multi-hit collision with cooldown between hits
- Trump's money throw uses MoneyBill particles with physics simulation
- Text effects are implemented via TextEffect class for special moves
- Mobile controls are implemented with virtual joystick and action buttons
- Mobile restart button appears after game over
- Throw animations no longer rotate the thrown character
- Blocking logic has been fixed to prevent movement lock
- Ghost trail system is implemented but disabled by default (press 'G' to toggle)

## Update Checklist
When making changes, update:
1. Recent Changes section with date and description
2. Character moves if new moves added
3. Project structure if files added/removed
4. Technical details if systems changed
5. Git repository info if branches/remotes change

---
Last Updated: 2025-08-02 (Ghost trail system & walk cycle fixes)