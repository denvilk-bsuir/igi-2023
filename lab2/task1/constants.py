
SENTENCES = r"(?P<sentence>(?P<word>((?P<reg>(?P<type>Mr|Mrs|No|pp|St|no|Jr|Bros|Sr|etc|vs|esp|Fig|fig|Jan|Feb|Mar|Apr|Jun|Jul|Aug|Sep|Sept|Oct|Okt|Nov|Dec|Ph\.D|PhD|al|cf|Inc|Ms|Gen|Sen|Prof|Dr|Corp|Co|Adj|Adm|Adv|Asst|Bart|Bldg|Brig|Bros|Capt|Cmdr|Col|Comdr|Con|Corp|Cpl|DR|Dr|Drs|Ens|Gen|Gov|Hon|Hr|Hosp|Insp|Lt|MM|MR|MRS|MS|Maj|Messrs|Mlle|Mme|Mr|Mrs|Ms|Msgr|Op|Ord|Pfc|Ph|Prof|Pvt|Rep|Reps|Res|Rev|Rt|Sen|Sens|Sfc|Sgt|Sr|St|Supt|Surg)\.\s*(?P<subword>\w+))|([\w0-9,'\-\"\"]+))\s*)+(?P<sign>(\.|\;|\!|\?|\.\.\.))\s*)"

WORDS = r'[\w+\'0-9]+'
