## SpellCorrect

A django based REST interface for correcting spellings, can be tested at -
https://spell-correct.herokuapp.com/spellcorrect/

## Demo Usage

- Using `GET` method: pass the words separated by comma to `words` parameter
```bash
 curl 'https://spell-correct.herokuapp.com/spellcorrect/?format=json&words=prouciation,speling,apliction'
 ```
- Same can also be achieved with `POST` request by passing words as a json:
```bash
curl -d '{"words":["prouciation", "speling", "apliction"]}' \
     -H 'Content-Type: application/json' \
     'https://spell-correct.herokuapp.com/spellcorrect/'
```

## Development Setup

- Download repository or clone with:
```bash
git clone https://github.com/krsoninikhil/spell-correct.git
```
- Change directory to it and install requirements with:
```bash
sudo pip install -r requirements.txt
```
- It uses `djangorestframework` for api implementation.
- Runs tests using:
```bash
python manage.py test
```
- If all tests are passing, start the server with:
```bash
python manage.py runserver
```

## Correction Part

- `spell_correct.py` in `app` directory is responsible for correction.
- Currently it uses implementation from this [Peter Norvig's tutorial on
spelling correction](http://norvig.com/spell-correct.html).
- It also implements Soundex method to correct spelling errors explained
[here](https://nlp.stanford.edu/IR-book/html/htmledition/phonetic-correction-1.html),
which can be accessed by passing `method` parameter to api with
`soundex` as value (`norgiv` is default).
- Soudex implementation is not providing enough accuracy.
- I've tried optimizing Norvig's algorithm based on
[Faroo's approach](http://blog.faroo.com/2012/06/07/), but this requires
enough memory to enhace the performance that could it could not start on my
16 GB system.
- I'm currently working on character level RNN based approach to achieve
better performance and accuracy.

## License

[MIT License](https://nks.mit-license.org/)
