# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

The recommendation system is unfair when a user wants to find a song using any metric other than genre and mood. Since they carry the most weight and there isn't any additional logic to fallback on other features like energy, the model performs poorly when the user profile does not specify a mood/genre inside songs.csv. The user is also able to input energy levels and bpm that exceed the cap, which is a another limitation of the system. Overall, in the next iteration of the program, I want a more dynamic score calculation (one that falls back on other features if mood/genre match is not found), and also introduce gaurd rails for input edge cases.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

For the most part, the model behaved as I expected. Since the formula was not too complicated, I understood almost all the outputs. It made sense that most of the first reccomendations in each of the user profiles was influenced heavily by mood and genre. I was expecting to run into this issue, so I have made example profiles where the genre/mood conflicts with the rest of the features. However, I was not anticipating the user entering a numerical value that exceeds the cap for some features. Also, there were profiles that used "not-a-genre" (basically blank), which was a unexpected edge case I haven't thought about.

No need for numeric metrics unless you created some.

Example profiles tested (11)

```
Top Recommendations for {'genre': 'rock', 'mood': 'angry', 'energy': 0.9}
# Compare to pop/sad below: same energy, totally different top songs
========================================

1. Storm Runner by Voltline
   Score: 0.45
   Reasons:
     - Matches your favorite genre 'rock' (+0.30)
     - Energy (0.91) is close to your target (+0.15)

2. Iron Wolves by Grave Circuit
   Score: 0.44
   Reasons:
     - Matches your favorite mood 'angry' (+0.30)
     - Energy (0.97) is close to your target (+0.14)

3. Neon Pulse Rising by DJ Kilowatt
   Score: 0.15
   Reasons:
     - Energy (0.88) is close to your target (+0.15)

4. Gym Hero by Max Pulse
   Score: 0.15
   Reasons:
     - Energy (0.93) is close to your target (+0.15)

5. Sunrise City by Neon Echo
   Score: 0.14
   Reasons:
     - Energy (0.82) is close to your target (+0.14)
```

```
Top Recommendations for {'genre': 'jazz', 'mood': 'relaxed', 'energy': 0.4, 'tempo_bpm': 90.0}
# Compare to chill lofi below: shared mood pulls both to same top pick
========================================

1. Coffee Shop Stories by Slow Stereo
   Score: 0.85
   Reasons:
     - Matches your favorite genre 'jazz' (+0.30)
     - Matches your favorite mood 'relaxed' (+0.30)
     - Energy (0.37) is close to your target (+0.15)
     - Tempo (90.0 bpm) is close to your target (+0.10)

2. Focus Flow by LoRoom
   Score: 0.24
   Reasons:
     - Energy (0.4) is close to your target (+0.15)
     - Tempo (80.0 bpm) is close to your target (+0.10)

3. Dusty Road Home by Wren & Iron
   Score: 0.24
   Reasons:
     - Energy (0.45) is close to your target (+0.14)
     - Tempo (88.0 bpm) is close to your target (+0.10)

4. Midnight Coding by LoRoom
   Score: 0.24
   Reasons:
     - Energy (0.42) is close to your target (+0.15)
     - Tempo (78.0 bpm) is close to your target (+0.09)

5. Island Drift by Sunny Roots
   Score: 0.23
   Reasons:
     - Energy (0.5) is close to your target (+0.14)
     - Tempo (92.0 bpm) is close to your target (+0.10)
```

```
Top Recommendations for {'genre': 'chill lofi', 'mood': 'relaxed', 'energy': 0.3, 'tempo_bpm': 70.0}
# Same "relaxed" mood as jazz profile above, different genre entirely
========================================

1. Coffee Shop Stories by Slow Stereo
   Score: 0.53
   Reasons:
     - Matches your favorite mood 'relaxed' (+0.30)
     - Energy (0.37) is close to your target (+0.14)
     - Tempo (90.0 bpm) is close to your target (+0.09)

2. Spacewalk Thoughts by Orbit Bloom
   Score: 0.24
   Reasons:
     - Energy (0.28) is close to your target (+0.15)
     - Tempo (60.0 bpm) is close to your target (+0.10)

3. Library Rain by Paper Lanterns
   Score: 0.24
   Reasons:
     - Energy (0.35) is close to your target (+0.14)
     - Tempo (72.0 bpm) is close to your target (+0.10)

4. Winter Piano Letters by Elena Voss
   Score: 0.24
   Reasons:
     - Energy (0.25) is close to your target (+0.14)
     - Tempo (66.0 bpm) is close to your target (+0.10)

5. Focus Flow by LoRoom
   Score: 0.23
   Reasons:
     - Energy (0.4) is close to your target (+0.13)
     - Tempo (80.0 bpm) is close to your target (+0.10)
```

```
Top Recommendations for {'genre': 'breakup', 'mood': 'sad', 'energy': 0.2, 'tempo_bpm': 55.0}
# No genre/mood match here, so low energy alone drives the ranking
========================================

1. Winter Piano Letters by Elena Voss
   Score: 0.24
   Reasons:
     - Energy (0.25) is close to your target (+0.14)
     - Tempo (66.0 bpm) is close to your target (+0.09)

2. Spacewalk Thoughts by Orbit Bloom
   Score: 0.24
   Reasons:
     - Energy (0.28) is close to your target (+0.14)
     - Tempo (60.0 bpm) is close to your target (+0.10)

3. Library Rain by Paper Lanterns
   Score: 0.22
   Reasons:
     - Energy (0.35) is close to your target (+0.13)
     - Tempo (72.0 bpm) is close to your target (+0.09)

4. Focus Flow by LoRoom
   Score: 0.21
   Reasons:
     - Energy (0.4) is close to your target (+0.12)
     - Tempo (80.0 bpm) is close to your target (+0.09)

5. Coffee Shop Stories by Slow Stereo
   Score: 0.21
   Reasons:
     - Energy (0.37) is close to your target (+0.12)
     - Tempo (90.0 bpm) is close to your target (+0.08)
```

```
Top Recommendations for {'genre': 'pop', 'mood': 'sad', 'energy': 0.9}
# Compare to rock/angry above: same energy, genre alone changes winner
========================================

1. Gym Hero by Max Pulse
   Score: 0.45
   Reasons:
     - Matches your favorite genre 'pop' (+0.30)
     - Energy (0.93) is close to your target (+0.15)

2. Sunrise City by Neon Echo
   Score: 0.44
   Reasons:
     - Matches your favorite genre 'pop' (+0.30)
     - Energy (0.82) is close to your target (+0.14)

3. Storm Runner by Voltline
   Score: 0.15
   Reasons:
     - Energy (0.91) is close to your target (+0.15)

4. Neon Pulse Rising by DJ Kilowatt
   Score: 0.15
   Reasons:
     - Energy (0.88) is close to your target (+0.15)

5. Iron Wolves by Grave Circuit
   Score: 0.14
   Reasons:
     - Energy (0.97) is close to your target (+0.14)
```

```
Top Recommendations for {'genre': 'pop', 'mood': 'happy', 'energy': 1.5}
# Invalid energy shrinks that term's boost but genre/mood still wins
========================================

1. Sunrise City by Neon Echo
   Score: 0.65
   Reasons:
     - Matches your favorite genre 'pop' (+0.30)
     - Matches your favorite mood 'happy' (+0.30)
     - Energy (0.82) is close to your target (+0.05)

2. Gym Hero by Max Pulse
   Score: 0.36
   Reasons:
     - Matches your favorite genre 'pop' (+0.30)
     - Energy (0.93) is close to your target (+0.06)

3. Rooftop Lights by Indigo Parade
   Score: 0.34
   Reasons:
     - Matches your favorite mood 'happy' (+0.30)
     - Energy (0.76) is close to your target (+0.04)

4. Iron Wolves by Grave Circuit
   Score: 0.07
   Reasons:
     - Energy (0.97) is close to your target (+0.07)

5. Storm Runner by Voltline
   Score: 0.06
   Reasons:
     - Energy (0.91) is close to your target (+0.06)
```

```
Top Recommendations for {'genre': 'rock', 'mood': 'angry', 'energy': -0.5}
# Compare to energy 0.9 version above: same winners, lower total scores
========================================

1. Storm Runner by Voltline
   Score: 0.24
   Reasons:
     - Matches your favorite genre 'rock' (+0.30)

2. Iron Wolves by Grave Circuit
   Score: 0.23
   Reasons:
     - Matches your favorite mood 'angry' (+0.30)

3. Winter Piano Letters by Elena Voss
   Score: 0.04
   Reasons:
     - Energy (0.25) is close to your target (+0.04)

4. Spacewalk Thoughts by Orbit Bloom
   Score: 0.03
   Reasons:
     - Energy (0.28) is close to your target (+0.03)

5. Library Rain by Paper Lanterns
   Score: 0.02
   Reasons:
     - Energy (0.35) is close to your target (+0.02)
```

```
Top Recommendations for {}
# No preferences at all, so every song ties at a score of zero
========================================

1. Sunrise City by Neon Echo
   Score: 0.00
   Reasons:
     - No strong matches with your preferences

2. Midnight Coding by LoRoom
   Score: 0.00
   Reasons:
     - No strong matches with your preferences

3. Storm Runner by Voltline
   Score: 0.00
   Reasons:
     - No strong matches with your preferences

4. Library Rain by Paper Lanterns
   Score: 0.00
   Reasons:
     - No strong matches with your preferences

5. Gym Hero by Max Pulse
   Score: 0.00
   Reasons:
     - No strong matches with your preferences
```

```
Top Recommendations for {'genre': 'pop', 'mood': 'happy', 'energy': 0.5, 'tempo_bpm': 400.0}
# Extreme tempo barely matters since tempo carries the least weight
========================================

1. Sunrise City by Neon Echo
   Score: 0.66
   Reasons:
     - Matches your favorite genre 'pop' (+0.30)
     - Matches your favorite mood 'happy' (+0.30)
     - Energy (0.82) is close to your target (+0.10)

2. Rooftop Lights by Indigo Parade
   Score: 0.37
   Reasons:
     - Matches your favorite mood 'happy' (+0.30)
     - Energy (0.76) is close to your target (+0.11)

3. Gym Hero by Max Pulse
   Score: 0.35
   Reasons:
     - Matches your favorite genre 'pop' (+0.30)
     - Energy (0.93) is close to your target (+0.09)

4. Island Drift by Sunny Roots
   Score: 0.10
   Reasons:
     - Energy (0.5) is close to your target (+0.15)

5. Dusty Road Home by Wren & Iron
   Score: 0.09
   Reasons:
     - Energy (0.45) is close to your target (+0.14)
```

```
Top Recommendations for {'genre': 'xyz-not-a-genre', 'mood': 'not-a-mood', 'energy': 0.5}
# Compare to empty profile above: valid energy still ranks songs
========================================

1. Island Drift by Sunny Roots
   Score: 0.15
   Reasons:
     - Energy (0.5) is close to your target (+0.15)

2. Dusty Road Home by Wren & Iron
   Score: 0.14
   Reasons:
     - Energy (0.45) is close to your target (+0.14)

3. Slow Burn by Velvet Hour
   Score: 0.14
   Reasons:
     - Energy (0.55) is close to your target (+0.14)

4. Midnight Coding by LoRoom
   Score: 0.14
   Reasons:
     - Energy (0.42) is close to your target (+0.14)

5. Focus Flow by LoRoom
   Score: 0.14
   Reasons:
     - Energy (0.4) is close to your target (+0.14)
```

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
