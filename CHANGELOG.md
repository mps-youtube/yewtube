# CHANGELOG


## v2.12.1 (2025-01-05)

### Bug Fixes

- Bump yt-dlp version to next stable release
  ([`1c79f11`](https://github.com/mps-youtube/yewtube/commit/1c79f112f64f82474ea323d2793411a6b4fde1a1))

### Chores

- Fixes #1303 1300 https > 0.28 throws proxy can not be passed as argument error
  ([`7ab2fe2`](https://github.com/mps-youtube/yewtube/commit/7ab2fe2cf05e4ad77093ebbb0eb11b597b6682d9))

### Documentation

- Demonstrate how to use existing mpv input bindings
  ([#1289](https://github.com/mps-youtube/yewtube/pull/1289),
  [`2d89c3f`](https://github.com/mps-youtube/yewtube/commit/2d89c3fb946b683778501d896f149c534586bb67))

demonstrate how to use existing mpv input bindings


## v2.12.0 (2024-09-11)

### Chores

- Clean up setup.cfg
  ([`dfa42a2`](https://github.com/mps-youtube/yewtube/commit/dfa42a2afeed3e4130870af8eecd6a54d05d4340))


## v2.11.7 (2024-09-11)

### Bug Fixes

- Semantic_release version for pypi setup.py was stuck
  ([`f29e0b3`](https://github.com/mps-youtube/yewtube/commit/f29e0b33241ae50e04fb4d2b0b8308be328eef82))


## v2.11.6 (2024-09-11)

### Bug Fixes

- Wheel_recipe.sh
  ([`5005c1a`](https://github.com/mps-youtube/yewtube/commit/5005c1a79e09049a57b8427678062f20cf377a72))

### Chores

- Update author email
  ([`6a5641c`](https://github.com/mps-youtube/yewtube/commit/6a5641cfdf209a9c87783178b61b9ea348aed6b9))


## v2.11.5 (2024-09-11)


## v2.11.4 (2024-09-11)


## v2.11.3 (2024-09-11)

### Documentation

- Extend upgrade instructions ([#1249](https://github.com/mps-youtube/yewtube/pull/1249),
  [`f62a5fd`](https://github.com/mps-youtube/yewtube/commit/f62a5fd96f97806f35a015df21274e0debf0c8e3))

This adds the pip / pipx commands to upgrade all the dependencies. This makes directed actions like
  https://github.com/mps-youtube/yewtube/issues/1225#issuecomment-1493400886 unnecessary.


## v2.10.5 (2023-08-29)

### Bug Fixes

- #1243 bumped yt-dlp version
  ([`9ed4921`](https://github.com/mps-youtube/yewtube/commit/9ed4921693443bb92eaddbafbfadeba8839b4e04))

- #1243 bumped yt-dlp version
  ([`4461d0c`](https://github.com/mps-youtube/yewtube/commit/4461d0c8e2b6f47c2919e6ae932eb28c8102e5cd))

Thanks to @galgot


## v2.10.4 (2023-06-14)

### Bug Fixes

- #806 - pressing q doesn't stops playback when in repeat mode
  ([`645617a`](https://github.com/mps-youtube/yewtube/commit/645617accd1fda316b22aa81270917adae9d2712))

### Chores

- Use pipenv
  ([`2edd0dd`](https://github.com/mps-youtube/yewtube/commit/2edd0ddb4f8e9b450fac7218995a8dc8dc6f1ea1))


## v2.10.3 (2023-06-14)


## v2.10.2 (2023-03-22)

### Bug Fixes

- #837 crashes if the video is blocked by the copyright holder
  ([`c472c7a`](https://github.com/mps-youtube/yewtube/commit/c472c7a7e428122e147422df84a819b58e790455))

- Shuffle all throwing error "object does not support item assignment"
  ([`13fb47b`](https://github.com/mps-youtube/yewtube/commit/13fb47b8113a0ccfc884852065f587a4de94eb0d))


## v2.10.1 (2023-03-21)

### Bug Fixes

- #980 added pylast as dependency in req.txt
  ([`48cc757`](https://github.com/mps-youtube/yewtube/commit/48cc757a4e89c551d6bcbbe54614f11fedeabbe9))


## v2.10.0 (2023-03-21)


## v2.9.4 (2023-01-28)

### Bug Fixes

- Semantic release python pypi receipe
  ([`495629a`](https://github.com/mps-youtube/yewtube/commit/495629ab78534a1a6b36a2adae2bc6c200083706))

- Updated readme metioned yewtube as fork of mpsyt
  ([`385d6a7`](https://github.com/mps-youtube/yewtube/commit/385d6a77708991d1d27371067023b253c2d14770))

### Documentation

- Added collaborators and contributors page
  ([`f258403`](https://github.com/mps-youtube/yewtube/commit/f25840322dea95d80b591732a2d3224047c020fc))

- Fix broken readme links
  ([`6d2d723`](https://github.com/mps-youtube/yewtube/commit/6d2d723e13d18854ab0a2c8c4364ff5a1c99b5d9))

### Features

- Added subtitle suppport for vlc related to #331
  ([`96f2efd`](https://github.com/mps-youtube/yewtube/commit/96f2efd8352bf5cd3d3310214af69e0e6db37f5b))


## v2.9.2 (2023-01-26)

### Bug Fixes

- Remove pyreadline dependency (#105) ([#107](https://github.com/mps-youtube/yewtube/pull/107),
  [`19e4148`](https://github.com/mps-youtube/yewtube/commit/19e4148242380b543a4825962716550114984f11))

It's unmaintained and yewtube works fine without it

Co-authored-by: Francesco Gazzetta <fgaz@fgaz.me>


## v2.9.1 (2023-01-26)

### Bug Fixes

- #50 - brought back download audio file
  ([`b46dab4`](https://github.com/mps-youtube/yewtube/commit/b46dab47e61c68efa0e51836a8cc9141d15d9e87))


## v2.9.0 (2022-10-20)

### Bug Fixes

- #76 video pops up
  ([`eaeff58`](https://github.com/mps-youtube/yewtube/commit/eaeff58f94e2fd89706e42fdab6b8e82ef770941))

### Features

- **mplayer**: Set cache ([#93](https://github.com/mps-youtube/yewtube/pull/93),
  [`16d3a18`](https://github.com/mps-youtube/yewtube/commit/16d3a186fb9feb24530e1f07b211062c44a515a0))


## v2.8.5 (2022-09-08)

### Bug Fixes

- #75 program crashes while creating custom playlist and saving it without playing
  ([`2552eff`](https://github.com/mps-youtube/yewtube/commit/2552eff602683fbd28bc6841768bf6cf585fc960))

- Enable quit-watch-later in mpv #77
  ([`079e440`](https://github.com/mps-youtube/yewtube/commit/079e44088260c938dc3ae71cd55146fb51de653e))

Allows pressing shift-q to quit so mpv saves the video position and allows resuming on next play

- **main**: Handle error when setting locale ([#86](https://github.com/mps-youtube/yewtube/pull/86),
  [`ecd117c`](https://github.com/mps-youtube/yewtube/commit/ecd117ca1ef753509b78082d6f919c9bc2b1756b))

fix #85(main): handle error when setting locale

### Documentation

- Added common issues file. ([#91](https://github.com/mps-youtube/yewtube/pull/91),
  [`4b69e5e`](https://github.com/mps-youtube/yewtube/commit/4b69e5ee96ed36efa9a68f6315322ed3d44d1e3d))

* Added common issues file with some instructions for MacOS

* Modified readme with extra information about the common issue file

Co-authored-by: fazli.zekiqi <fazli.zekiqi@cepheid.com>

### Refactoring

- **main**: Use logging instead of warning ([#88](https://github.com/mps-youtube/yewtube/pull/88),
  [`32e7935`](https://github.com/mps-youtube/yewtube/commit/32e79356a96ec6e9e8e61496d39aff3c79d58da6))


## v2.8.4 (2022-05-05)

### Bug Fixes

- #53 viewing playlists uploaded by a user is back
  ([`f201cb5`](https://github.com/mps-youtube/yewtube/commit/f201cb5f4cd45b9341ced6b549fc35a57e85eb9f))


## v2.8.3 (2022-04-25)

### Bug Fixes

- #45 fetch all videos of a playlist
  ([`261f468`](https://github.com/mps-youtube/yewtube/commit/261f4687668c6c05415102c66587a27518bbac10))

- #67 vlc dummy Interface does not work with live channels
  ([`2d4637b`](https://github.com/mps-youtube/yewtube/commit/2d4637b04b6f738ab832b3beacab1e490e99a518))

- Save full playlists by name and all its videos
  ([`d69a959`](https://github.com/mps-youtube/yewtube/commit/d69a9594c5824d97201774e81444b75aea93e861))


## v2.8.2 (2022-03-17)

### Bug Fixes

- #63 module album search crash
  ([`3f2fcfb`](https://github.com/mps-youtube/yewtube/commit/3f2fcfb27bb60928282d1a4a68adff22980f5938))


## v2.8.1 (2022-03-08)

### Bug Fixes

- #24 colorama support for windows
  ([`9cf2616`](https://github.com/mps-youtube/yewtube/commit/9cf261615a52f6ac64b6fb28390db2a71a7ab470))

- #28 show changelog with `help new` command
  ([`d52b65d`](https://github.com/mps-youtube/yewtube/commit/d52b65d0c0cd8708020a2d6788102d82d8ebeee5))

- #35 remove api key instructions
  ([`4f1fee3`](https://github.com/mps-youtube/yewtube/commit/4f1fee3b711b2383b2704fba39bdce772894cc75))

- #37 use `set pages` command to config how many search result pages to show
  ([`2baec5f`](https://github.com/mps-youtube/yewtube/commit/2baec5fd11c0edf88d3543dd81333c5ecf67c918))

- #38 improved help menu responsiveness
  ([`972b4ef`](https://github.com/mps-youtube/yewtube/commit/972b4efdb5fe8f5d3295b1c3fe607d209e7d39b6))

- #39 key error 'data'
  ([`834ed5b`](https://github.com/mps-youtube/yewtube/commit/834ed5b0af5f92e1233e8ba327327654f67f61a0))

- #44 dont run init when importing mps_youtube
  ([`a072c22`](https://github.com/mps-youtube/yewtube/commit/a072c22e2781160bca79d0164e46e49f07ac28e1))

- #54 play video using youtube short link
  ([`92d1c77`](https://github.com/mps-youtube/yewtube/commit/92d1c776d4bcc47509becadc5ba9248477dc0dcc))

- 26 album search working now without youtube api
  ([`9c3ae03`](https://github.com/mps-youtube/yewtube/commit/9c3ae03b8c0ae006f1b9a917e4330270fec2f929))

- Bring back requirements.txt to life
  ([`ff6e59d`](https://github.com/mps-youtube/yewtube/commit/ff6e59d75834c61d72ec6bbc92f5eb339cc82607))

- Buffersize warning
  ([`d185c3f`](https://github.com/mps-youtube/yewtube/commit/d185c3fdf8d520bcb4595f5e458d6022a7b6d1aa))

- Check for app updates
  ([`eabfb52`](https://github.com/mps-youtube/yewtube/commit/eabfb5233c7b87c5f300ebc41250a3f52db07411))

- Default player priority is vlc > mpv > mplayer on first install fixed #16
  ([`35409eb`](https://github.com/mps-youtube/yewtube/commit/35409eb31cc67f03c50589e02cdff2ad08fe4911))

- Don't crash if playlists / history file has invalid youtube id fixed #24
  ([`323d5d8`](https://github.com/mps-youtube/yewtube/commit/323d5d822cefc23889665d71cfffe9e40750433b))

- Playlists are working again fixed #18
  ([`bfceee4`](https://github.com/mps-youtube/yewtube/commit/bfceee493261d099c85bf2c4c9e79e5710e9799f))

- Use mkdocs instead of sphinx docs
  ([`32a2e9c`](https://github.com/mps-youtube/yewtube/commit/32a2e9cdddac3ebb458d7bdcd793ed83ccc2fdf0))

* build(setup): extras_require mkdocs

- package mkdocstrings-python-legacy

* refactor: check sys.stdout.encoding once

also isort module

* docs: mkdocs

- skip_files for test files

* docs(CONTRIBUTING): mkdocs

- **g**: Mpv msglevel
  ([`062b125`](https://github.com/mps-youtube/yewtube/commit/062b12503a8fa15dc720cf3ac91f001b74a5cf10))

- **mplayer**: _get_mplayer_version
  ([`ab21c5d`](https://github.com/mps-youtube/yewtube/commit/ab21c5d1bc872ed482bf482ad37949129c1e4f78))

- isort module - type hint - function doc - return value type hint for func

- **mpris**: Handle no data on time-pos
  ([`8bb29d3`](https://github.com/mps-youtube/yewtube/commit/8bb29d33825ad826e51d9d8eada32a9b7bd10ffd))

- **util.uea_pad**: Handle AttributeError on t.split
  ([`1643266`](https://github.com/mps-youtube/yewtube/commit/1643266f21ccf7a99481a1615b4a53c4fbabc878))

also isort import

### Build System

- Include changelog
  ([`18390f5`](https://github.com/mps-youtube/yewtube/commit/18390f5ffa3c812a41b0ec09c5b0f2077304f575))

- **setup**: Add requests
  ([`397eddd`](https://github.com/mps-youtube/yewtube/commit/397eddd0146e04e95e6cc0598741bae8055a3e32))

### Continuous Integration

- Python-app
  ([`f40ca1a`](https://github.com/mps-youtube/yewtube/commit/f40ca1a557974929da3cc0c599d1f9342b4cdfa9))

- **python-app**: Workflows based on origin/develop
  ([`3d117ad`](https://github.com/mps-youtube/yewtube/commit/3d117ad49ed8630873dd070f474e6641007fd01a))

- only run pytest - use matrix for python version and os

### Features

- Use yewtube over tor using torsocks 🔥
  ([`1e9c4ce`](https://github.com/mps-youtube/yewtube/commit/1e9c4ce5992528286f552c8b563daef4abf9566a))

- **helptext**: Help changelog
  ([`0643941`](https://github.com/mps-youtube/yewtube/commit/06439411d7a78fe6701f7313e9b3b0720248a197))

- **setup**: Extras dependencies for mpris
  ([`936e890`](https://github.com/mps-youtube/yewtube/commit/936e8909b5212eda3a64e8b93be79d4353e6d646))

### Refactoring

- Reset to upstream
  ([`dc4af72`](https://github.com/mps-youtube/yewtube/commit/dc4af721aa90fe79c492f9f1ae1f4a698049a085))

### Testing

- Uea_pad
  ([`22b4564`](https://github.com/mps-youtube/yewtube/commit/22b4564e618aceb49bad34428e45e9ecf25907e6))

- **mplayer**: _get_mplayer_version
  ([`9c2350c`](https://github.com/mps-youtube/yewtube/commit/9c2350c87daed2a52460b4e9ad72ba4b11e7796f))

use default func behavior when no mplayer found

- **mpris**: Test_mpris.setproperty
  ([`10ec94a`](https://github.com/mps-youtube/yewtube/commit/10ec94adb7dd5cb0e00c58d1700039ee04479e21))

- **Mpris2Controller**: Init
  ([`cb977ec`](https://github.com/mps-youtube/yewtube/commit/cb977eca7b8aa02c5cecf27c5c5a6e104c50c8c4))

- **test_main**: Skip test without attribute after fork
  ([`35ded20`](https://github.com/mps-youtube/yewtube/commit/35ded20a8ee1392c731bd6a35f1f3a2d10897c92))


## v2.6.4 (2022-02-16)

### Bug Fixes

- Duplicate changelog and readme files
  ([`0265ef7`](https://github.com/mps-youtube/yewtube/commit/0265ef7507b539791684bdcf40b30ddaafc525e8))


## v2.6.3 (2022-02-16)

### Bug Fixes

- Welcome from semantic release python
  ([`c237a68`](https://github.com/mps-youtube/yewtube/commit/c237a6808869062036f5196775352c1504eafe06))

- **setup**: Use semantic versioning
  ([`2e100e7`](https://github.com/mps-youtube/yewtube/commit/2e100e761ede07a402bb975d428f1d6837154813))

### Build System

- **setup**: Fix long_description_content_type
  ([`db30143`](https://github.com/mps-youtube/yewtube/commit/db30143d8630d848098be4166e4a2c517a7b7772))

### Features

- **setup**: Restrict pyreadline3 to windows only
  ([`7ebbf20`](https://github.com/mps-youtube/yewtube/commit/7ebbf208812a45d6bba7e152dacab8c30a2b6843))

- **setup**: Restrict python version
  ([`b9bc61f`](https://github.com/mps-youtube/yewtube/commit/b9bc61f9ac2bd4935a47a7a76d21a730cf869449))

### Refactoring

- **setup**: Check for minimum python 3.6
  ([`f5b5d73`](https://github.com/mps-youtube/yewtube/commit/f5b5d733f4a8e115f48b335c3950efbb945d375f))


## v0.2.8 (2018-02-17)


## v0.2.7 (2016-06-27)


## v0.2.6 (2016-01-01)


## v0.2.5 (2015-06-01)


## v0.2.4 (2015-05-13)


## v0.2.3 (2015-02-17)


## v0.2.2 (2015-02-14)


## v0.2.1 (2014-11-27)


## v0.2.0 (2014-11-25)
