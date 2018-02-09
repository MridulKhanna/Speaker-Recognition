# Speaker-Recognition
Identification of speaker with voice given as input

Like in speech recognition,what is being said is identified whereas in Speaker recognition system,the speaker is identified.We plan to achieve three models in this project:-

1.Achieving higher accuracy with noisy input samples.

2.Differentiating between mimic voice and original voice.

3.Differentiating between computer generated and true human voice.

Motivation-

1.Currently a widely popular bank HSBC is implementing it to get the details of the user by identifying his/her voice.

2.It can serve as a great purpose for physically challenged people.

3.It can cut down the time in BPO's.

The voice sample is given as the input and the Gaussian white noise is removed from it using Mahalanobis distance.The voice is processed further and MFCC features are exracted from it in the form of tuples.The MFCC features are then trained using deep neural networks.
Keras library is being used for deep neural networks.

