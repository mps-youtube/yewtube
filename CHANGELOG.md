# CHANGELOG

## v2.11.4 (2024-09-11)

## v2.11.3 (2024-09-11)

## v2.11.2 (2024-09-11)

## v2.11.1 (2024-09-11)

## v2.11.0 (2024-09-11)

### Documentation

* docs: extend upgrade instructions (#1249)

This adds the pip / pipx commands to upgrade all the dependencies. This makes directed actions like https://github.com/mps-youtube/yewtube/issues/1225#issuecomment-1493400886 unnecessary. ([`f62a5fd`](https://github.com/mps-youtube/yewtube/commit/f62a5fd96f97806f35a015df21274e0debf0c8e3))

### Unknown

* Fix Issue #1064 and #1283: User and Channel searches to return all videos including optional filtering of search terms (#1282) (#1288)

* Updated the all_videos_from_channel function to return all videos from a channel, not just the first page of playlist results (previous method only returned up to 100 videos max).

* Updated the usersearch_id function to filter the returned videos by search term in the title or description. This restores the ability to search a user&#39;s videos.

Co-authored-by: Robert Hill &lt;robert.hill@uphillsolutions.tech&gt; ([`a5574cf`](https://github.com/mps-youtube/yewtube/commit/a5574cff5dd28bf39c0f6686d219c743435db5af))

* Update COLLABORATORS.md ([`0c1e39d`](https://github.com/mps-youtube/yewtube/commit/0c1e39d51f5d4c6e1bea25b72c00900aab991e37))

* Update project URL and version maintenance (#1262)

* Update project URL

* Update __version__ in setup.py

This suppresses the update notifications

* help new: more accurate helptext

`help new` doesn&#39;t actually check whether there&#39;s a new version,
it shows the changelog for the latest release no matter what.
Update helptext to reflect this. ([`42cfda0`](https://github.com/mps-youtube/yewtube/commit/42cfda07ddc690e5ef1c42aa704a3d221f877b28))

* fix syntax warnings on 3.12 (#1263) ([`f8c1f1d`](https://github.com/mps-youtube/yewtube/commit/f8c1f1d14cb21879ded6fdfba2e919b652692410))

* added a notice ([`e39978a`](https://github.com/mps-youtube/yewtube/commit/e39978a8deeeef371a0466eba701b872cdec7c6e))

## v2.10.5 (2023-08-29)

### Fix

* fix: #1243 bumped yt-dlp version ([`9ed4921`](https://github.com/mps-youtube/yewtube/commit/9ed4921693443bb92eaddbafbfadeba8839b4e04))

* fix: #1243 bumped yt-dlp version

Thanks to @galgot ([`4461d0c`](https://github.com/mps-youtube/yewtube/commit/4461d0c8e2b6f47c2919e6ae932eb28c8102e5cd))

### Unknown

* Merge pull request #1244 from mps-youtube/develop

fixed: #1243 bumped yt-dlp version ([`1c05626`](https://github.com/mps-youtube/yewtube/commit/1c0562602ba3c87eb061aeb5c38252c9809eed1f))

## v2.10.4 (2023-06-14)

### Chore

* chore: use pipenv ([`2edd0dd`](https://github.com/mps-youtube/yewtube/commit/2edd0ddb4f8e9b450fac7218995a8dc8dc6f1ea1))

### Fix

* fix: #806 - pressing q doesn&#39;t stops playback when in repeat mode ([`645617a`](https://github.com/mps-youtube/yewtube/commit/645617accd1fda316b22aa81270917adae9d2712))

## v2.10.3 (2023-06-14)

### Unknown

* Merge pull request #1235 from mps-youtube/develop

fix: no color support &amp; suffle all bug fix ([`d5e19b2`](https://github.com/mps-youtube/yewtube/commit/d5e19b247107183021b0ac300771d2018d53f68b))

* Merge pull request #1226 from prettykool/develop

fix: #1042  `NO_COLOR` support ([`ed28213`](https://github.com/mps-youtube/yewtube/commit/ed28213014888a6c2cadd0f3afeecae65aa13d06))

* Add `NO_COLOR` support ([`cd905ec`](https://github.com/mps-youtube/yewtube/commit/cd905ec5c5dabcb63b4c37a1a9e12cd74d360bb1))

* Merge branch &#39;develop&#39; of github.com:mps-youtube/yewtube into develop ([`df939d3`](https://github.com/mps-youtube/yewtube/commit/df939d3ea721d63d73efa4eb4174e5c5f1e857aa))

* Merge pull request #1224 from mps-youtube/master

get changes from upstream ([`b984982`](https://github.com/mps-youtube/yewtube/commit/b98498257a0867e9805d138d956ae491ee4747a1))

* Merge pull request #1223 from mps-youtube/develop

Develop ([`60a526c`](https://github.com/mps-youtube/yewtube/commit/60a526c26089e9f01f9918cfdf47498f0926237b))

* Merge pull request #1222 from mps-youtube/master

merge changes from upstream ([`8ea0b49`](https://github.com/mps-youtube/yewtube/commit/8ea0b49cf08fc52d081c035fdd286044b8342924))

## v2.10.2 (2023-03-22)

### Fix

* fix: #837 crashes if the video is blocked by the copyright holder ([`c472c7a`](https://github.com/mps-youtube/yewtube/commit/c472c7a7e428122e147422df84a819b58e790455))

* fix: shuffle all throwing error &#34;object does not support item assignment&#34; ([`13fb47b`](https://github.com/mps-youtube/yewtube/commit/13fb47b8113a0ccfc884852065f587a4de94eb0d))

### Unknown

* Merge branch &#39;master&#39; of github.com:mps-youtube/yewtube ([`32f88ec`](https://github.com/mps-youtube/yewtube/commit/32f88ecec4fef1450d12f3c8f9aaa765bb40665e))

* Merge pull request #1221 from mps-youtube/master

multiple improvements ([`655acc3`](https://github.com/mps-youtube/yewtube/commit/655acc377feba8fd0ef65e736326d4bfe333e6a2))

* Merge pull request #1218 from pataquets/dockerfile-improvements

Dockerfile minor improvements ([`08323c5`](https://github.com/mps-youtube/yewtube/commit/08323c54afaee804894782db8ff413df47ded2df))

* Dockerfile minor improvements:
- Prevent `pip install` from persisting cache (improves size).
- Correctly set `DEBIAN_ENVIRONMENT` env variable. ([`0fbede3`](https://github.com/mps-youtube/yewtube/commit/0fbede397bf8ba90eeae720fe3facbb5d195dc1f))

## v2.10.1 (2023-03-21)

### Fix

* fix: #980 added pylast as dependency in req.txt ([`48cc757`](https://github.com/mps-youtube/yewtube/commit/48cc757a4e89c551d6bcbbe54614f11fedeabbe9))

### Unknown

* Update COLLABORATORS.md ([`493b161`](https://github.com/mps-youtube/yewtube/commit/493b1615a6bea98a5513f0f2d97ddbfe5eed33b4))

* Update COLLABORATORS.md ([`c9a01ab`](https://github.com/mps-youtube/yewtube/commit/c9a01ab8f6f734760ff5dbaf558f478fd34bb3c4))

## v2.10.0 (2023-03-21)

### Unknown

* Merge branch &#39;master&#39; of github.com:mps-youtube/yewtube ([`51e7e17`](https://github.com/mps-youtube/yewtube/commit/51e7e1715abd86e65300895a687db6d88d8ac003))

* Merge pull request #1215 from mps-youtube/develop

fix: check for mpv config dir ([`a20be95`](https://github.com/mps-youtube/yewtube/commit/a20be95610215aa299b820a3a6a2159cf8735e69))

* Merge pull request #1209 from fractal161/mpv-conf

fix: check for mpv configuration directory ([`3d4e720`](https://github.com/mps-youtube/yewtube/commit/3d4e7209f4034630859cb865515e178f5302aa2f))

* check for mpv configuration directory ([`f165369`](https://github.com/mps-youtube/yewtube/commit/f165369c9f05ea7a7b6940eb34dd7fe64d48c0bf))

## v2.9.4 (2023-01-28)

### Documentation

* docs: added collaborators and contributors page ([`f258403`](https://github.com/mps-youtube/yewtube/commit/f25840322dea95d80b591732a2d3224047c020fc))

* docs: fix broken readme links ([`6d2d723`](https://github.com/mps-youtube/yewtube/commit/6d2d723e13d18854ab0a2c8c4364ff5a1c99b5d9))

### Feature

* feat: added subtitle suppport for vlc related to #331 ([`96f2efd`](https://github.com/mps-youtube/yewtube/commit/96f2efd8352bf5cd3d3310214af69e0e6db37f5b))

### Fix

* fix: semantic release python pypi receipe ([`495629a`](https://github.com/mps-youtube/yewtube/commit/495629ab78534a1a6b36a2adae2bc6c200083706))

* fix: updated readme metioned yewtube as fork of mpsyt ([`385d6a7`](https://github.com/mps-youtube/yewtube/commit/385d6a77708991d1d27371067023b253c2d14770))

### Unknown

* Create semantic-release-python.yml ([`56f0972`](https://github.com/mps-youtube/yewtube/commit/56f09729a6e1209e78aaf237fba31188c8fa1e5e))

* Merge pull request #1205 from mps-youtube/develop

merge changes ([`65dca2f`](https://github.com/mps-youtube/yewtube/commit/65dca2fb069ba336170fa8243f8e0935bbbaf0ec))

* Merge pull request #891 from sankeerth95/develop

fix: correcting inconsistent return statement ([`496b776`](https://github.com/mps-youtube/yewtube/commit/496b7760e396549a76c782ed00b9170422319065))

* correcting inconsistent return statement ([`3cdb12a`](https://github.com/mps-youtube/yewtube/commit/3cdb12a454ffffa9c409842a117cbcca0e6df9a1))

* Merge pull request #1203 from iamtalhaasghar/master

merge yewtube codebase in mps-youtube ([`42ce836`](https://github.com/mps-youtube/yewtube/commit/42ce83694e7512df4655a0d975b321c51be59254))

## v2.9.2 (2023-01-26)

### Fix

* fix: remove pyreadline dependency (#105) (#107)

It&#39;s unmaintained and yewtube works fine without it

Co-authored-by: Francesco Gazzetta &lt;fgaz@fgaz.me&gt; ([`19e4148`](https://github.com/mps-youtube/yewtube/commit/19e4148242380b543a4825962716550114984f11))

### Unknown

* Merge branch &#39;master&#39; of github.com:iamtalhaasghar/yewtube ([`ba3502d`](https://github.com/mps-youtube/yewtube/commit/ba3502d921be1e5e267ceebf2e40ae10c1f41c7b))

## v2.9.1 (2023-01-26)

### Fix

* fix: #50 - brought back download audio file ([`b46dab4`](https://github.com/mps-youtube/yewtube/commit/b46dab47e61c68efa0e51836a8cc9141d15d9e87))

### Unknown

* related to #84 ([`b9e69a8`](https://github.com/mps-youtube/yewtube/commit/b9e69a8217d4c6931522efd295da1eb5caf0c635))

* fix typos ([`47e4730`](https://github.com/mps-youtube/yewtube/commit/47e47308c756650718ced9008d8485c948ababd1))

## v2.9.0 (2022-10-20)

### Feature

* feat(mplayer): set cache (#93) ([`16d3a18`](https://github.com/mps-youtube/yewtube/commit/16d3a186fb9feb24530e1f07b211062c44a515a0))

### Fix

* fix: #76 video pops up ([`eaeff58`](https://github.com/mps-youtube/yewtube/commit/eaeff58f94e2fd89706e42fdab6b8e82ef770941))

### Unknown

* moved to wiki section ([`e8ce805`](https://github.com/mps-youtube/yewtube/commit/e8ce8057cf96770139d2355ebefe5f9197eb107a))

## v2.8.5 (2022-09-08)

### Documentation

* docs: Added common issues file. (#91)

* Added common issues file with some instructions for MacOS

* Modified readme with extra information about the common issue file

Co-authored-by: fazli.zekiqi &lt;fazli.zekiqi@cepheid.com&gt; ([`4b69e5e`](https://github.com/mps-youtube/yewtube/commit/4b69e5ee96ed36efa9a68f6315322ed3d44d1e3d))

### Fix

* fix: #75 program crashes while creating custom playlist and saving it without playing ([`2552eff`](https://github.com/mps-youtube/yewtube/commit/2552eff602683fbd28bc6841768bf6cf585fc960))

* fix(main): handle error when setting locale (#86)

fix #85(main): handle error when setting locale ([`ecd117c`](https://github.com/mps-youtube/yewtube/commit/ecd117ca1ef753509b78082d6f919c9bc2b1756b))

* fix: Enable quit-watch-later in mpv #77

Allows pressing shift-q to quit so mpv saves the video position and allows
resuming on next play ([`079e440`](https://github.com/mps-youtube/yewtube/commit/079e44088260c938dc3ae71cd55146fb51de653e))

### Refactor

* refactor(main): use logging instead of warning (#88) ([`32e7935`](https://github.com/mps-youtube/yewtube/commit/32e79356a96ec6e9e8e61496d39aff3c79d58da6))

### Unknown

* Implement &#39;shuffle all&#39; and &#39;play all&#39; (#81)

fix #73: Implement &#39;shuffle all&#39; and &#39;play all&#39; ([`fd1b9ea`](https://github.com/mps-youtube/yewtube/commit/fd1b9ea84a3391245709ca39ff53f0e254eea53a))

* Update requirements.txt ([`e1b26da`](https://github.com/mps-youtube/yewtube/commit/e1b26da50eb885c917dff554e7ecab4e8fc4f699))

* userpl requires youtube search python version 1.6.5 ([`6d959bd`](https://github.com/mps-youtube/yewtube/commit/6d959bd49c90dcccf7e292a5921b517853d06f00))

## v2.8.4 (2022-05-05)

### Fix

* fix: #53 viewing playlists uploaded by a user is back ([`f201cb5`](https://github.com/mps-youtube/yewtube/commit/f201cb5f4cd45b9341ced6b549fc35a57e85eb9f))

## v2.8.3 (2022-04-25)

### Fix

* fix: #45 fetch all videos of a playlist ([`261f468`](https://github.com/mps-youtube/yewtube/commit/261f4687668c6c05415102c66587a27518bbac10))

* fix: save full playlists by name and all its videos ([`d69a959`](https://github.com/mps-youtube/yewtube/commit/d69a9594c5824d97201774e81444b75aea93e861))

* fix: #67  vlc dummy Interface does not work with live channels ([`2d4637b`](https://github.com/mps-youtube/yewtube/commit/2d4637b04b6f738ab832b3beacab1e490e99a518))

## v2.8.2 (2022-03-17)

### Fix

* fix: #63 module album search crash ([`3f2fcfb`](https://github.com/mps-youtube/yewtube/commit/3f2fcfb27bb60928282d1a4a68adff22980f5938))

### Unknown

* minor bug ([`bb89051`](https://github.com/mps-youtube/yewtube/commit/bb89051f3e796f003c179766fac69f917824bd7f))

* mpris (#64)

mpris ([`67e5be7`](https://github.com/mps-youtube/yewtube/commit/67e5be7b5aa02d25f1242fbd105325f6374bef36))

## v2.8.1 (2022-03-08)

### Build

* build: include changelog ([`18390f5`](https://github.com/mps-youtube/yewtube/commit/18390f5ffa3c812a41b0ec09c5b0f2077304f575))

* build(setup): add requests ([`397eddd`](https://github.com/mps-youtube/yewtube/commit/397eddd0146e04e95e6cc0598741bae8055a3e32))

### Ci

* ci(python-app): workflows based on origin/develop

- only run pytest
- use matrix for python version and os ([`3d117ad`](https://github.com/mps-youtube/yewtube/commit/3d117ad49ed8630873dd070f474e6641007fd01a))

* ci: python-app ([`f40ca1a`](https://github.com/mps-youtube/yewtube/commit/f40ca1a557974929da3cc0c599d1f9342b4cdfa9))

### Feature

* feat(helptext): help changelog ([`0643941`](https://github.com/mps-youtube/yewtube/commit/06439411d7a78fe6701f7313e9b3b0720248a197))

* feat(setup): extras dependencies for mpris ([`936e890`](https://github.com/mps-youtube/yewtube/commit/936e8909b5212eda3a64e8b93be79d4353e6d646))

* feat: use yewtube over tor using torsocks 🔥 ([`1e9c4ce`](https://github.com/mps-youtube/yewtube/commit/1e9c4ce5992528286f552c8b563daef4abf9566a))

### Fix

* fix: #54 play video using youtube short link ([`92d1c77`](https://github.com/mps-youtube/yewtube/commit/92d1c776d4bcc47509becadc5ba9248477dc0dcc))

* fix: use mkdocs instead of sphinx docs

* build(setup): extras_require mkdocs

* build(setup): extras_require mkdocs

- package mkdocstrings-python-legacy

* refactor: check sys.stdout.encoding once

also isort module

* docs: mkdocs

- skip_files for test files

* docs(CONTRIBUTING): mkdocs ([`32a2e9c`](https://github.com/mps-youtube/yewtube/commit/32a2e9cdddac3ebb458d7bdcd793ed83ccc2fdf0))

* fix: #37 use `set pages` command to config how many search result pages to show ([`2baec5f`](https://github.com/mps-youtube/yewtube/commit/2baec5fd11c0edf88d3543dd81333c5ecf67c918))

* fix: #44 dont run init when importing mps_youtube ([`a072c22`](https://github.com/mps-youtube/yewtube/commit/a072c22e2781160bca79d0164e46e49f07ac28e1))

* fix: #39 key error &#39;data&#39; ([`834ed5b`](https://github.com/mps-youtube/yewtube/commit/834ed5b0af5f92e1233e8ba327327654f67f61a0))

* fix(mpris): handle no data on time-pos ([`8bb29d3`](https://github.com/mps-youtube/yewtube/commit/8bb29d33825ad826e51d9d8eada32a9b7bd10ffd))

* fix: #38 improved help menu responsiveness ([`972b4ef`](https://github.com/mps-youtube/yewtube/commit/972b4efdb5fe8f5d3295b1c3fe607d209e7d39b6))

* fix: #35 remove api key instructions ([`4f1fee3`](https://github.com/mps-youtube/yewtube/commit/4f1fee3b711b2383b2704fba39bdce772894cc75))

* fix: #24 colorama support for windows ([`9cf2616`](https://github.com/mps-youtube/yewtube/commit/9cf261615a52f6ac64b6fb28390db2a71a7ab470))

* fix: #28 show changelog with `help new` command ([`d52b65d`](https://github.com/mps-youtube/yewtube/commit/d52b65d0c0cd8708020a2d6788102d82d8ebeee5))

* fix: 26 album search working now without youtube api ([`9c3ae03`](https://github.com/mps-youtube/yewtube/commit/9c3ae03b8c0ae006f1b9a917e4330270fec2f929))

* fix: check for app updates ([`eabfb52`](https://github.com/mps-youtube/yewtube/commit/eabfb5233c7b87c5f300ebc41250a3f52db07411))

* fix: don&#39;t crash if playlists / history file has invalid youtube id fixed #24 ([`323d5d8`](https://github.com/mps-youtube/yewtube/commit/323d5d822cefc23889665d71cfffe9e40750433b))

* fix: playlists are working again fixed #18 ([`bfceee4`](https://github.com/mps-youtube/yewtube/commit/bfceee493261d099c85bf2c4c9e79e5710e9799f))

* fix: buffersize warning ([`d185c3f`](https://github.com/mps-youtube/yewtube/commit/d185c3fdf8d520bcb4595f5e458d6022a7b6d1aa))

* fix(g): mpv msglevel ([`062b125`](https://github.com/mps-youtube/yewtube/commit/062b12503a8fa15dc720cf3ac91f001b74a5cf10))

* fix: default player priority is vlc &gt; mpv &gt; mplayer on first install fixed #16 ([`35409eb`](https://github.com/mps-youtube/yewtube/commit/35409eb31cc67f03c50589e02cdff2ad08fe4911))

* fix(mplayer): _get_mplayer_version

- isort module
- type hint
- function doc
- return value type hint for func ([`ab21c5d`](https://github.com/mps-youtube/yewtube/commit/ab21c5d1bc872ed482bf482ad37949129c1e4f78))

* fix(util.uea_pad): handle AttributeError on t.split

also isort import ([`1643266`](https://github.com/mps-youtube/yewtube/commit/1643266f21ccf7a99481a1615b4a53c4fbabc878))

* fix: bring back requirements.txt to life ([`ff6e59d`](https://github.com/mps-youtube/yewtube/commit/ff6e59d75834c61d72ec6bbc92f5eb339cc82607))

### Refactor

* refactor: reset to upstream ([`dc4af72`](https://github.com/mps-youtube/yewtube/commit/dc4af721aa90fe79c492f9f1ae1f4a698049a085))

### Test

* test(mpris): test_mpris.setproperty ([`10ec94a`](https://github.com/mps-youtube/yewtube/commit/10ec94adb7dd5cb0e00c58d1700039ee04479e21))

* test(Mpris2Controller): init ([`cb977ec`](https://github.com/mps-youtube/yewtube/commit/cb977eca7b8aa02c5cecf27c5c5a6e104c50c8c4))

* test(mplayer): _get_mplayer_version

use default func behavior when no mplayer found ([`9c2350c`](https://github.com/mps-youtube/yewtube/commit/9c2350c87daed2a52460b4e9ad72ba4b11e7796f))

* test: uea_pad ([`22b4564`](https://github.com/mps-youtube/yewtube/commit/22b4564e618aceb49bad34428e45e9ecf25907e6))

* test(test_main): skip test without attribute after fork ([`35ded20`](https://github.com/mps-youtube/yewtube/commit/35ded20a8ee1392c731bd6a35f1f3a2d10897c92))

### Unknown

* delete github workflows ([`31b695b`](https://github.com/mps-youtube/yewtube/commit/31b695be14ff3bb735c25c69274c9cfdaf4f7a8d))

* play_url and yt_url related to #59 (#60)

* related to #49

* refactor(play): play_url

- documentation
- isort
- use boolean for yt_url&#39;s print_title
- type hint

* refactor(search): yt_url

- isort
- documentation
- only work on unique video id
- fix video title when printing
- print title when there is only video title
- use boolean for print_title parameter

* docs(pafy): extract_video_id

- isort
- documentation

Co-authored-by: Talha Asghar &lt;talhaasghar.contact@simplelogin.fr&gt;

Co-authored-by: rachmadani haryono &lt;rachmadaniHaryono@users.noreply.github.com&gt; ([`7409188`](https://github.com/mps-youtube/yewtube/commit/7409188acc57d1a4faaea8b787289784edc57da5))

* related to #49 ([`d7fa4e9`](https://github.com/mps-youtube/yewtube/commit/d7fa4e914d138152f2e1ee92726a18d46f3f144b))

* broken contribution page link ([`4460b5e`](https://github.com/mps-youtube/yewtube/commit/4460b5eb8cc5604852386c9f4d13c587cc5c1810))

* Merge branch &#39;master&#39; of github.com:iamtalhaasghar/yewtube ([`42f6496`](https://github.com/mps-youtube/yewtube/commit/42f649689cf059903ff4a099b96f20f4154c75bd))

* Merge pull request #43 from rachmadaniHaryono/feature/changelog

feat: help changelog ([`d768571`](https://github.com/mps-youtube/yewtube/commit/d76857189cf00b3a67ba15c432d10e54a9c93903))

* Update MANIFEST.in ([`c0812de`](https://github.com/mps-youtube/yewtube/commit/c0812de3597a0c67514995b3ee4f0c25c62493d9))

* Merge pull request #42 from rachmadaniHaryono/feature/mpris-setup

extra requirement for mpris ([`5a9656a`](https://github.com/mps-youtube/yewtube/commit/5a9656a56f24ae3db375aefa7be8cc6e800dae2c))

* Merge pull request #41 from rachmadaniHaryono/feature/mpris

test Mpris2Controller.setproperty for time-pos ([`f61620c`](https://github.com/mps-youtube/yewtube/commit/f61620c64a7a478e32072ca375c4f3a90dfb578d))

* Merge branch &#39;master&#39; of https://github.com/iamtalhaasghar/yewtube into feature/mpris ([`2375e00`](https://github.com/mps-youtube/yewtube/commit/2375e00ddbcf88f2bbc5c1d4dcbbfd9273fe1b08))

* Merge branch &#39;master&#39; of https://github.com/iamtalhaasghar/yewtube into feature/mpris ([`8fe1f55`](https://github.com/mps-youtube/yewtube/commit/8fe1f55f058e523a794f68c6a0988b371eeb5b43))

* Merge branch &#39;master&#39; of github.com:iamtalhaasghar/yewtube ([`318fcb2`](https://github.com/mps-youtube/yewtube/commit/318fcb277c8b38fc552fb12dc4dec39b8fe0568c))

* added logo ([`0aefa76`](https://github.com/mps-youtube/yewtube/commit/0aefa769d117283a90b63353491a984811a4781b))

* Merge branch &#39;master&#39; of github.com:iamtalhaasghar/yewtube ([`4c0d93b`](https://github.com/mps-youtube/yewtube/commit/4c0d93b36e070eb458970d7ea5d5764476bb0b4f))

* Set theme jekyll-theme-hacker ([`fd952d6`](https://github.com/mps-youtube/yewtube/commit/fd952d603d55af2e3f4eb9ac5520bc3ac0a042cf))

* Set theme jekyll-theme-cayman ([`7de825f`](https://github.com/mps-youtube/yewtube/commit/7de825f80af62e77b161e3f83f34708b2f142413))

* Update CHANGELOG.md ([`b8486cf`](https://github.com/mps-youtube/yewtube/commit/b8486cf41d317f78e869b89291f4d2b712c43e53))

* display main menu / previous songs list if requested album is not found ([`25cf2ae`](https://github.com/mps-youtube/yewtube/commit/25cf2ae1bb729175fb82a5d3446c4a571bb815a2))

* enter command which caused bug ([`067d1d9`](https://github.com/mps-youtube/yewtube/commit/067d1d999830616f9dfd39ec602270663ff39542))

* typo fix ([`df51f9e`](https://github.com/mps-youtube/yewtube/commit/df51f9ee926bdc2bb20c1d4e77829b617f8f7567))

* fix #27 channel search working without youtube api key ([`440ab17`](https://github.com/mps-youtube/yewtube/commit/440ab17108f64316fc74e476715445b939372d69))

* fix #25 videos can now be played by url ([`b9d4650`](https://github.com/mps-youtube/yewtube/commit/b9d4650ce78fd4ab5f1735a3c9558569dcad70ad))

* Merge pull request #23 from iamtalhaasghar/develop

fix: buffersize warning ([`08967b0`](https://github.com/mps-youtube/yewtube/commit/08967b0670774ad7728db39a76944303b1bc1551))

* Update CHANGELOG.md ([`bb943a0`](https://github.com/mps-youtube/yewtube/commit/bb943a0121c13b10228daadad5bf83e0f6a96b70))

* how to install latest vs table version ([`69be64c`](https://github.com/mps-youtube/yewtube/commit/69be64c605c1861bae7e14ef79ebfb8e119af91e))

* Merge pull request #22 from rachmadaniHaryono/bugfix/mpv

fix: mpv message level fixed #21 ([`1c8876c`](https://github.com/mps-youtube/yewtube/commit/1c8876c3b59ca0e7de7e80b242b852b4d1cc2bb7))

* Merge pull request #20 from iamtalhaasghar/develop

Develop ([`d2384e9`](https://github.com/mps-youtube/yewtube/commit/d2384e9da88a19610b6b16d2b072f8ceb80028f5))

* Merge pull request #19 from rachmadaniHaryono/bugfix/mplayer-version

fix _get_mplayer_version ([`ba70beb`](https://github.com/mps-youtube/yewtube/commit/ba70beb707c8b300ae2e3ddb6eebb74993fda7d1))

* Merge pull request #17 from rachmadaniHaryono/bugfix/attribute-error

test uea_pad ([`376ebe1`](https://github.com/mps-youtube/yewtube/commit/376ebe1be5442e84b089a223472a742da1b56008))

* Merge branch &#39;develop&#39; of https://github.com/iamtalhaasghar/yewtube into bugfix/attribute-error ([`ebf62f5`](https://github.com/mps-youtube/yewtube/commit/ebf62f591b4dbb2fb2b240020fffe7ef80c043bf))

* Merge branch &#39;develop&#39; of https://github.com/iamtalhaasghar/yewtube into bugfix/attribute-error ([`ae6bad4`](https://github.com/mps-youtube/yewtube/commit/ae6bad4050ec8186deae94af69bf55257ba0f2a3))

* Merge remote-tracking branch &#39;upstream/develop&#39; into bugfix/attribute-error ([`6078793`](https://github.com/mps-youtube/yewtube/commit/6078793d55edfbf09eb3de415a0b8d43a8dcbac6))

* moved old changelogs CHANGELOG &gt; CHANGELOG.md ([`f845604`](https://github.com/mps-youtube/yewtube/commit/f84560441dac6d8872c9baaffbe35aeab9acb37c))

## v2.6.4 (2022-02-16)

### Fix

* fix: duplicate changelog and readme files ([`0265ef7`](https://github.com/mps-youtube/yewtube/commit/0265ef7507b539791684bdcf40b30ddaafc525e8))

## v2.6.3 (2022-02-16)

### Build

* build(setup): fix long_description_content_type ([`db30143`](https://github.com/mps-youtube/yewtube/commit/db30143d8630d848098be4166e4a2c517a7b7772))

### Feature

* feat(setup): restrict python version ([`b9bc61f`](https://github.com/mps-youtube/yewtube/commit/b9bc61f9ac2bd4935a47a7a76d21a730cf869449))

* feat(setup): restrict pyreadline3 to windows only ([`7ebbf20`](https://github.com/mps-youtube/yewtube/commit/7ebbf208812a45d6bba7e152dacab8c30a2b6843))

### Fix

* fix: welcome from semantic release python ([`c237a68`](https://github.com/mps-youtube/yewtube/commit/c237a6808869062036f5196775352c1504eafe06))

* fix(setup): use semantic versioning ([`2e100e7`](https://github.com/mps-youtube/yewtube/commit/2e100e761ede07a402bb975d428f1d6837154813))

### Refactor

* refactor(setup): check for minimum python 3.6 ([`f5b5d73`](https://github.com/mps-youtube/yewtube/commit/f5b5d733f4a8e115f48b335c3950efbb945d375f))

### Unknown

* setup python-semantic-versioning ([`53b7ea3`](https://github.com/mps-youtube/yewtube/commit/53b7ea3dc9c8974f4c060477c5f2d2f1b4bbd7f4))

* Delete python-publish.yml ([`7a1d688`](https://github.com/mps-youtube/yewtube/commit/7a1d68863fb720e791b98b1dd946e108312ba812))

* use semantic release ([`5a54ddc`](https://github.com/mps-youtube/yewtube/commit/5a54ddc457600ad966d4670182e48b76b92a27aa))

* show dislikes using video info command only as its too costly to make multiple requests for each video ([`19e3d8e`](https://github.com/mps-youtube/yewtube/commit/19e3d8e7b25a528def641f6dd69caad1bdebf808))

* add hour to version number scheme ([`a823e36`](https://github.com/mps-youtube/yewtube/commit/a823e36e7b0eb81e5b272dd87900c24cff7d8a61))

* add requests in dependency ([`5f26359`](https://github.com/mps-youtube/yewtube/commit/5f263592beadb4ba7e530afae17d53d5b6d152f6))

* wheel upload recipe ([`d1af41a`](https://github.com/mps-youtube/yewtube/commit/d1af41a30a5162365bd634056c35611c79b74ed4))

* Update python-publish.yml ([`3b46e8d`](https://github.com/mps-youtube/yewtube/commit/3b46e8d79cb28a482838afc761e813cba61bcf0f))

* show dislikes by default return youtube dislikes working fine relates to #1180 ([`b15451c`](https://github.com/mps-youtube/yewtube/commit/b15451c151d9fa1043be0465647c773fbee876e1))

* fixed #11 show extra columns if user wants ([`31cd67e`](https://github.com/mps-youtube/yewtube/commit/31cd67e15e92e6a38e17e4715023508062ebccf1))

* show dislikes, likes and keywords with `i &lt;video_num&gt;` command ([`3b885b2`](https://github.com/mps-youtube/yewtube/commit/3b885b25f270a28656035059601f7f646415c120))

* Update setup.py ([`0e7ecf1`](https://github.com/mps-youtube/yewtube/commit/0e7ecf11b23092b70ad4531ce3dac8ccc4b51bcd))

* Delete release.yml ([`27d6e9d`](https://github.com/mps-youtube/yewtube/commit/27d6e9dd96503265900a3c0f59cdff60083d97f1))

* Update setup.py ([`36f35a1`](https://github.com/mps-youtube/yewtube/commit/36f35a1dd5718b88f25d92624e685b644f1b39af))

* × python setup.py egg_info did not run successfully. ([`8c96dd2`](https://github.com/mps-youtube/yewtube/commit/8c96dd2f998734a22455c7e52876fc0332ec3151))

* Merge branch &#39;develop&#39; of github.com:iamtalhaasghar/yewtube into develop ([`572ca4e`](https://github.com/mps-youtube/yewtube/commit/572ca4e735eaeb993eaf5a3bbfbdacd92f41b71b))

* Merge pull request #15 from rachmadaniHaryono/feature/setup

update python and package ([`4108987`](https://github.com/mps-youtube/yewtube/commit/41089877e1f781f3d6e24a73310dfe9b1b4ccaa5))

* restricted pyreadline to linux ([`a40ede7`](https://github.com/mps-youtube/yewtube/commit/a40ede737ceba261e5b36a2ad744c4b0030040a0))

* fixed #14 load video info without youtube api relates to #1191 ([`0ed1eac`](https://github.com/mps-youtube/yewtube/commit/0ed1eac4bf73e92bf0cece3d8792653f1c64a43b))

* fixed #13 show comments without youtube api relates to #1191 ([`a1226e6`](https://github.com/mps-youtube/yewtube/commit/a1226e6c194ca445e89e536e61210507401c7f40))

* prettier version number ([`65cc68f`](https://github.com/mps-youtube/yewtube/commit/65cc68f980bcad5f30a834f17c18e44731dd8e57))

* Merge branch &#39;develop&#39; of github.com:iamtalhaasghar/yewtube into develop ([`9bb0fa8`](https://github.com/mps-youtube/yewtube/commit/9bb0fa8d5cab6451f3f01facef308b92f8fa4168))

* upload packages to pypi on every tag push ([`5d05f28`](https://github.com/mps-youtube/yewtube/commit/5d05f28ad05e078c2a1f87afca7c6bc9923936b3))

* use semantic versioning with date ([`8bc6acf`](https://github.com/mps-youtube/yewtube/commit/8bc6acfb346fb82d00080f1d953191ac6c4782bd))

* changed version numbering scheme ([`295da12`](https://github.com/mps-youtube/yewtube/commit/295da12aa5f7fa3a7317b8199dcd68c1486b8c2f))

* added github release workflow ([`9bd63b6`](https://github.com/mps-youtube/yewtube/commit/9bd63b6669b81cd9e28e7dd6466aeea702f421b3))

* Update setup.py ([`0743b22`](https://github.com/mps-youtube/yewtube/commit/0743b221a3afd9941071b39238c15a8fa0d47db7))

* Update setup.py ([`a7f0b66`](https://github.com/mps-youtube/yewtube/commit/a7f0b66aa5663de4d7759dfa36c5b9e2b3146ea5))

* Update setup.py ([`33f78ac`](https://github.com/mps-youtube/yewtube/commit/33f78ac136728453bcb5805fda54d55c7e32ad2c))

* Update setup.py ([`118deea`](https://github.com/mps-youtube/yewtube/commit/118deea7758e327afa6c0f818d61e7e2837d8995))

* Update setup.py ([`2706e12`](https://github.com/mps-youtube/yewtube/commit/2706e1209d0788d81209485cf2929a340ce0af75))

* Update setup.py ([`85cf414`](https://github.com/mps-youtube/yewtube/commit/85cf414d6dd21ebdc35a20b409a23dad0aa0bf1d))

* Update __init__.py ([`c0308bf`](https://github.com/mps-youtube/yewtube/commit/c0308bfb184568a396488694ebd7b778564a3cea))

* Update VERSION ([`12306c9`](https://github.com/mps-youtube/yewtube/commit/12306c9a2ca8ffef424b949c2d4d27bd324fe7d1))

* Create python-publish.yml ([`699ee20`](https://github.com/mps-youtube/yewtube/commit/699ee20983140892855feed83410b6036843c629))

* Delete .github/workflows directory ([`75efc03`](https://github.com/mps-youtube/yewtube/commit/75efc032ef3a68fd4ed2d913cf12e1275940346d))

* Create python-publish.yml ([`2294666`](https://github.com/mps-youtube/yewtube/commit/22946669e23fe1f330652e6ed4ea196f1d7808f3))

* Merge pull request #9 from rachmadaniHaryono/bugfix/setup-readme

fix long_description_content_type ([`3ebd084`](https://github.com/mps-youtube/yewtube/commit/3ebd084963b133541afb33eeaffa8c4f1cab9154))

* #7 for now user &lt;username&gt;, user &lt;username&gt; / query, userpl &lt;username&gt; will all show you videos from that channels ([`d6a485e`](https://github.com/mps-youtube/yewtube/commit/d6a485e87254587186442da8902d5e3e3b7c753c))

* added comments ([`0316cc5`](https://github.com/mps-youtube/yewtube/commit/0316cc51c1ced163f51eae166c943331fb091bed))

* now it download videos without youtube api using yt-dlp fixed #1 ([`c9c5f27`](https://github.com/mps-youtube/yewtube/commit/c9c5f2745bba303df220405e18bf62761d2f6409))

* fixed #2 #1152 pyperclip is working perfectly fine now ([`d731e2a`](https://github.com/mps-youtube/yewtube/commit/d731e2ad757bf5c64d117fb6b9f98212b462efa5))

* fixed #1154 by setting buffersize to 0 ([`371e059`](https://github.com/mps-youtube/yewtube/commit/371e0593612ae2ee7d85a7fca5e06175229ca784))

* related to #1154 disabled warnings ([`82781c9`](https://github.com/mps-youtube/yewtube/commit/82781c977c9058dee11e167b45010514cbdbd877))

* fix NoneType does not have attribute expiry ([`fdeef36`](https://github.com/mps-youtube/yewtube/commit/fdeef36e945a88e4f23bd48b33a59a428c9931d9))

* available on pip ([`3fe9a6f`](https://github.com/mps-youtube/yewtube/commit/3fe9a6f0b877ad683869c410c19a9c71a7cc90eb))

* changed description of readme to reflect this as a fork of mps-youtube ([`eaec40e`](https://github.com/mps-youtube/yewtube/commit/eaec40e1a88ccdd12ac3865e690f2e56937e3e33))

* enjoy playlists without youtube_api ([`5490c24`](https://github.com/mps-youtube/yewtube/commit/5490c240e42905fcd202ef78a9d975d5e5554d4f))

* Merge branch &#39;develop&#39; of github.com:iamtalhaasghar/yewtube into develop ([`aab1b0e`](https://github.com/mps-youtube/yewtube/commit/aab1b0ec36a3cf5e959601ea13875e00ac7e6ebd))

* hide old pypi badges ([`3bcbd66`](https://github.com/mps-youtube/yewtube/commit/3bcbd66e45f6819fccba3f79f789f916d585c600))

* try to fetch upto 50 search results fixed #6 ([`4661a9c`](https://github.com/mps-youtube/yewtube/commit/4661a9c4c8fee3da81088c2e47def7d327e90eb9))

* bump version -&gt; 1.1.0 ([`3985498`](https://github.com/mps-youtube/yewtube/commit/3985498c51d7bad27b2ba8a0d1999578cda352cd))

* fixed #4 ([`3051217`](https://github.com/mps-youtube/yewtube/commit/3051217a716c324c4e935177e3a8fa2e19a52d84))

* remove output messages from yt-dlp ([`cdc0f01`](https://github.com/mps-youtube/yewtube/commit/cdc0f01b300aad79900cba886eafdd1ed571f1d1))

* now runs video without youtube api as well ([`0357cca`](https://github.com/mps-youtube/yewtube/commit/0357cca9ef7c251069a093374ec19ad2505e9ec8))

* removed pafy ([`b4f7a3b`](https://github.com/mps-youtube/yewtube/commit/b4f7a3bfbd9031522bd0bf51ac0e19fe34204b5e))

* bump version -&gt; 1.0.8 ([`c41cd8b`](https://github.com/mps-youtube/yewtube/commit/c41cd8b354509b05e0441b96fd1ddb2887c55984))

* no module named setup ([`762181e`](https://github.com/mps-youtube/yewtube/commit/762181e9f801265541ea7fe90ac8bdd9c060979e))

* now it doesn&#39;t requires youtube api related to #1123 #1119 ([`4801c3a`](https://github.com/mps-youtube/yewtube/commit/4801c3a5542b7318c493556e98ca5af2af821989))

* bump version -&gt; 1.0.5 ([`6f4fb12`](https://github.com/mps-youtube/yewtube/commit/6f4fb12346df92bf42ecb360999bbc4b82822fdd))

* minor bug ([`ce5ed0a`](https://github.com/mps-youtube/yewtube/commit/ce5ed0a3adbdbeb05c9367788f017d3df4dbe4fd))

* bump version -&gt; 1.0.4 ([`4bc33be`](https://github.com/mps-youtube/yewtube/commit/4bc33beb0e1e3b3e78f0117757d9da316beaa56d))

* added vlc_dummy_interface support for linux #1157 ([`4d66d89`](https://github.com/mps-youtube/yewtube/commit/4d66d89d1a2f230ab058cf1e3c50e911926a9e77))

* fixed minor bug NameError: name &#39;lines&#39; is not defined ([`e59c6c4`](https://github.com/mps-youtube/yewtube/commit/e59c6c488714ca8d6470c447939c2b378415a65f))

* manually bump version -&gt; 1.0.3 ([`f207c5d`](https://github.com/mps-youtube/yewtube/commit/f207c5d676169c39254935d03d61d7e63fef43ec))

* setup.py now determines version number dynamically ([`bcd9443`](https://github.com/mps-youtube/yewtube/commit/bcd944392291a9826cebc1d4c45b990fa198c2e2))

* set vlc as default player and removed default api_key ([`dec276f`](https://github.com/mps-youtube/yewtube/commit/dec276f7d06e2a8e44c9f79c2a954ad5307c98ed))

* removed circular import ([`99fdaa2`](https://github.com/mps-youtube/yewtube/commit/99fdaa2267605589f821dedc1b832d1ef5e0a089))

* added help message for vlc_dummy_interface ([`b6f36c3`](https://github.com/mps-youtube/yewtube/commit/b6f36c3d63ecc1e015b84421dd2bcc431105f0e8))

* added yewtube`s wiki link ([`8b189a1`](https://github.com/mps-youtube/yewtube/commit/8b189a1e09b825a19aea039ce1451f0038cc8f05))

* bump version 1.0.0 -&gt; 1.0.1 ([`27d5628`](https://github.com/mps-youtube/yewtube/commit/27d562822cfaeaa9515237783cd5352684bb7883))

* add new config option &#39;vlc_dummy_interface&#39; which when set to &#39;true&#39; will run vlc with no gui implements #1157 ([`1caa7f1`](https://github.com/mps-youtube/yewtube/commit/1caa7f1029930a81560e6eb3c5cedab7d479749e))

* 5 steps easy installation ([`ee7db37`](https://github.com/mps-youtube/yewtube/commit/ee7db370de9f4a05c57622792f1a38e796ad4c2f))

* installing pafy directly from source isn&#39;t a good idea so revert back ([`e471f52`](https://github.com/mps-youtube/yewtube/commit/e471f525280c293b1fa834a7f9ddc0fac5863e06))

* install pafy directly from source

Because latest build wheel hasn&#39;t been uploaded to pypi.org lately ([`5e2355f`](https://github.com/mps-youtube/yewtube/commit/5e2355f71e11d7888d5db442e9b3a7c09b48735e))

* add pyreadline in dependencies relates to #886 ([`4bf5ff9`](https://github.com/mps-youtube/yewtube/commit/4bf5ff9597077b56fc5a597a1a207766fe289447))

* add youtube_dl in requirements

So that you don&#39;t have to install youtube_dl separately. ([`eff6a30`](https://github.com/mps-youtube/yewtube/commit/eff6a3087e69d36546be1d825919abd223f06fe3))

* use dict.get(&#34;foo&#34;) instead of dict[&#34;foo&#34;] #1172 ([`7966a7a`](https://github.com/mps-youtube/yewtube/commit/7966a7a9178ecd3a87ae6dcb10f5fce45551d776))

* fixed typo in copyright section ([`cbca7e9`](https://github.com/mps-youtube/yewtube/commit/cbca7e90b91161de112c59a6034d1f5398554924))

* project name changed from mps-youtube to yewtube ([`6e83af8`](https://github.com/mps-youtube/yewtube/commit/6e83af8c20e277db543130a51886b907e7a4a2e0))

* added installation instructions

Install and Run mps-youtube in Isolated Environment using pipx. ([`436c58e`](https://github.com/mps-youtube/yewtube/commit/436c58e7f49f323932e61f665d63d5e32b1f9d01))

* Merge pull request #1120 from rjshrjndrn/patch-2

Adding repeat documentation ([`4c6ee0f`](https://github.com/mps-youtube/yewtube/commit/4c6ee0f8f4643fc1308e637b622d0337bf9bce1b))

* changing location for the repeat section ([`f752d78`](https://github.com/mps-youtube/yewtube/commit/f752d78276e3ec38e1d9fda343070dd729c6740b))

* Adding repeat documentation ([`2a78d79`](https://github.com/mps-youtube/yewtube/commit/2a78d79efdf0932d30fd725ae092381b47141026))

* Merge pull request #1027 from panasenco/develop

Gave mpv_usesock a default value on Windows. ([`7b95b9c`](https://github.com/mps-youtube/yewtube/commit/7b95b9c8cfab164958e9320c686fc0608126e9c7))

* Gave mpv_usesock a default value on Windows. Fixes mps-youtube/mps-youtube#825. ([`5d7956e`](https://github.com/mps-youtube/yewtube/commit/5d7956ebf01141bc28e81356d044152c4762656b))

* Merge pull request #1072 from tchernomax/fix_cache_error

move pafy.set_api_key before cache.load() ([`10ba3ad`](https://github.com/mps-youtube/yewtube/commit/10ba3ad682814d180157fa899eb751f20fb023fc))

* move pafy.set_api_key before cache.load()

else !1070 can happen ([`bb8ae4d`](https://github.com/mps-youtube/yewtube/commit/bb8ae4d53d18f5fb90feed2bd1c920a97fd694c7))

* Merge pull request #1102 from poyenc/bugfix/issue-1101

Fix issue #1101: ValueError raises when view video information ([`2567bc8`](https://github.com/mps-youtube/yewtube/commit/2567bc82415a9588c87dfdd2eb867e9f18815475))

* Fix ValueError raises when view video information

The video_info() employs strptime() to parse date string,
but it cannot handle the ISO 8601 time zone designator in
the end of string. For now we assume there is always a &#39;Z&#39;
time zone designator thus add &#39;Z&#39; in the strptime() format
string. ([`d8eec0b`](https://github.com/mps-youtube/yewtube/commit/d8eec0b54d4386ab60c48071410513999f72d7cb))

* Merge pull request #1099 from rjshrjndrn/patch-1

Readme Update ([`974c61d`](https://github.com/mps-youtube/yewtube/commit/974c61d9ab11881320f802b636b7dfed0e359a4f))

* Readme Update

1. For playing all search results
2. How to search for a playlist ([`b098534`](https://github.com/mps-youtube/yewtube/commit/b098534b812d37d0553b96e80201c8c46c51d7e8))

* Merge pull request #1104 from poyenc/bugfix/issue-1103

Fix issue #1103: Make MPRIS process error message more descriptive ([`91f2a06`](https://github.com/mps-youtube/yewtube/commit/91f2a06b83a0900c9e9e6842f499d30a741e4a45))

* Make MPRIS process error message more descriptive

When MPRIS process exited abnormally, show the exact
reason if we cannot successfully setup dbus. ([`da82be0`](https://github.com/mps-youtube/yewtube/commit/da82be099328fc32c2f2586938fc282b18fca41d))

* Merge pull request #1088 from francutura/develop

Fixed ValueError: time data does not match format ([`2217c29`](https://github.com/mps-youtube/yewtube/commit/2217c29c0517dffe434ca259e724c53cd97d7de5))

* Fixed ValueError: time data does not match format ([`e9356ac`](https://github.com/mps-youtube/yewtube/commit/e9356ac691c8d930a4867873399821bfcc3ee311))

* Merge pull request #1095 from jose-donato/patch-1

typo (youtybe-dl -&gt; youtube-dl) in README ([`fd83301`](https://github.com/mps-youtube/yewtube/commit/fd8330184707daf9f0d2456f9d480759c0cd9b5a))

* typo (youtybe-dl -&gt; youtube-dl) in README ([`8102275`](https://github.com/mps-youtube/yewtube/commit/8102275f2f0b8c81e62e84b3730903eefbc38042))

* Merge pull request #1065 from Atcold/patch-1

Transcode to mp3 from webm too ([`afab9fb`](https://github.com/mps-youtube/yewtube/commit/afab9fbc9ba61c646e406c6754e589c9c0c15c77))

* Transcode to mp3 from webm too ([`166b833`](https://github.com/mps-youtube/yewtube/commit/166b833cfbe9dd3e676c07cd0702f15f5f87717f))

* Merge pull request #1023 from Nojus297/filename_fix

Filename sanitation fix (#1009) ([`160fec9`](https://github.com/mps-youtube/yewtube/commit/160fec9fd3dbf26d2cb3f9dfb00b5e89a3d45082))

* Fix filename and folder sanitizing (#1009) ([`16ac040`](https://github.com/mps-youtube/yewtube/commit/16ac04096afe24c340775123748f3a370f2fc836))

* Add sanitize filename util function ([`68368da`](https://github.com/mps-youtube/yewtube/commit/68368da051bef0b33c773d78b9a26b46b92c492d))

* Merge pull request #1060 from felixonmars/patch-1

Correct a typo in RELEASING.md ([`af74a6d`](https://github.com/mps-youtube/yewtube/commit/af74a6dec46cfd6a13f8b957f8a1efd18ce680ef))

* Correct a typo in RELEASING.md ([`e1707af`](https://github.com/mps-youtube/yewtube/commit/e1707afb553e70fdccf4ab3835f8d44ccb12f597))

* Merge pull request #1053 from Deracinator/new-mpv-syntax

Update flags to use new mpv syntax ([`b808697`](https://github.com/mps-youtube/yewtube/commit/b808697133ec2ad7654953232d1e841b20aa7cc3))

* Update flags to use new mpv syntax,
see: https://github.com/mps-youtube/mps-youtube/issues/1052 ([`fd527b4`](https://github.com/mps-youtube/yewtube/commit/fd527b4a406bb6200fb314bc708b76bc57c9dbdc))

* Merge pull request #971 from jas32096/develop

Fix stream_details and player.play to reflect changes in override [Fixes #812] ([`ddfad46`](https://github.com/mps-youtube/yewtube/commit/ddfad464a968f3675c7aad0120646b4ab3674f71))

* Fix stream_details and player.play to reflect changes in override

This fixes the issue of live steams playing video, regardless of
the show_video setting, at least for mpv ([`c24a2ba`](https://github.com/mps-youtube/yewtube/commit/c24a2badb220336f530f531e6c6036c224994b3b))

* Merge pull request #1047 from Deracinator/bug

Fix bug that overwrites previously created playlist of the same name. ([`e43b36f`](https://github.com/mps-youtube/yewtube/commit/e43b36f7d6a1c4e547a8b388e104e0c826ee7ddc))

* Fix bug that overwrites previously created playlist of the same name.
For more information see:
https://github.com/mps-youtube/mps-youtube/issues/1046 ([`35d78b9`](https://github.com/mps-youtube/yewtube/commit/35d78b9bdb68f1b0bb88483d17b3babe73aa05ea))

* Merge pull request #1043 from zakkak/patch-1

Fix in typo &#39;MPRIS process exited of crashed&#39; ([`6b9a83a`](https://github.com/mps-youtube/yewtube/commit/6b9a83a3d04201aba7e40ce307a796bd841840d6))

* Fix in typo &#39;MPRIS process exited of crashed&#39; ([`5023df1`](https://github.com/mps-youtube/yewtube/commit/5023df108501709137ab75fba99bb33eb87d5669))

* Remove mention of master branch from RELEASING.md ([`381c362`](https://github.com/mps-youtube/yewtube/commit/381c362859dcd9b0f0b97b20373f2adf712520ac))

* Fix typo ([`7db90d7`](https://github.com/mps-youtube/yewtube/commit/7db90d7b5b591a0737edbbc2cf0f4d97c6a86cc7))

* Add RELEASING.md, describing the release process ([`6d7ad3a`](https://github.com/mps-youtube/yewtube/commit/6d7ad3ae169d4f571d71e4736e84dd82ec0c60a5))

* Merge pull request #1020 from adericbourg/patch-1

README: fix installation command for mpv ([`e083bfa`](https://github.com/mps-youtube/yewtube/commit/e083bfa535a9828ba6416447b8b1b52071f352e8))

* README: fix installation command for mpv ([`c5747c7`](https://github.com/mps-youtube/yewtube/commit/c5747c7839b32ff905a245afd4e02a379e596e91))

* Merge pull request #1029 from Nojus297/player_filenames_fix

Player filenames fix (#990) ([`3bacdfe`](https://github.com/mps-youtube/yewtube/commit/3bacdfe26bd95dc8f301a75cc8f9760654598cde))

* Show video title in vlc ([`a170ffc`](https://github.com/mps-youtube/yewtube/commit/a170ffc5db574a77a9524f67bd2482607128ee34))

* Show correct video title in mpv ([`bb3ed22`](https://github.com/mps-youtube/yewtube/commit/bb3ed22a7dda12575b44a0e639164b00688cf6f8))

* Use global config file in player classes ([`955deaf`](https://github.com/mps-youtube/yewtube/commit/955deaf23a278d8f238b131c5011403e73472435))

* Merge pull request #1001 from Nojus297/alignment_fix

Misalignment due to East East Asian chars fix ([`3b479cb`](https://github.com/mps-youtube/yewtube/commit/3b479cbba1a0928f707ea4b72314afe0a2156476))

* Format with uea_pad() in ListView.content() to fix misalignment ([`9d4d047`](https://github.com/mps-youtube/yewtube/commit/9d4d047df0b0a7a0b0abd10574804779d603477b))

* Use uea_pad() in generate_songlist_display() to fix misalignment ([`8409b00`](https://github.com/mps-youtube/yewtube/commit/8409b006e2340cd41cb6e10157ad5e29a10bb57c))

* Fix uea_pad function to use correct truncating ([`59f60d7`](https://github.com/mps-youtube/yewtube/commit/59f60d79af191c65f4a1a9aa3f5f8afa05ed92e8))

* Add correct_truncate function ([`442bf14`](https://github.com/mps-youtube/yewtube/commit/442bf14e993898d74767ff2a8c34a8d465e2cfae))

* Add .vscode to .gitignore ([`98ad8ec`](https://github.com/mps-youtube/yewtube/commit/98ad8ec643e77eb76dff6d05f176d97cceaf28c3))

* Merge pull request #998 from dt-rush/config_as_json

use json format for config file ([`8ee685a`](https://github.com/mps-youtube/yewtube/commit/8ee685aeea0c6ca1d8579d458e9f91ae0580522b))

* use json format for config file

Signed-off-by: dt-rush &lt;nickp@balena.io&gt; ([`fe44840`](https://github.com/mps-youtube/yewtube/commit/fe4484009f46fe549ddf796cebf9709d68508080))

* Merge pull request #940 from pirate486743186/edit-help

[minor]mention clearcache in help ([`6f9bd32`](https://github.com/mps-youtube/yewtube/commit/6f9bd32a70f3540204e3580942c4e8a6dde17f04))

* mention clearcache in help ([`28c876f`](https://github.com/mps-youtube/yewtube/commit/28c876f70ddee02ee4980619f20faa7221d20b23))

* Merge pull request #968 from pirate486743186/patch-4

[minor]web.archive.org for dead mps link ([`743843e`](https://github.com/mps-youtube/yewtube/commit/743843e7760ddb8f02edd3f3ea08c23e2c11f3e8))

* web.archive.org for dead mps link

for issue #957 ([`13fa4fc`](https://github.com/mps-youtube/yewtube/commit/13fa4fcfb5be2ec595a3cc251daa5e613084acf0))

* Merge pull request #991 from androidfanatic/patch-1

fix typo ([`05426f7`](https://github.com/mps-youtube/yewtube/commit/05426f75c0f35f2bf0037dc30f9ef09712da00f3))

* fix typo ([`6da11d0`](https://github.com/mps-youtube/yewtube/commit/6da11d06408419c8f5486d9c75a7bf9f09cef01a))

* Merge pull request #934 from vikramkashyap/optional_history

Option to turn on and off history recording ([`44fad52`](https://github.com/mps-youtube/yewtube/commit/44fad5215a5a8b3e828efc437ab0083751b19451))

* Added option to toggle play and input history recording ([`0aa6f68`](https://github.com/mps-youtube/yewtube/commit/0aa6f6891cf638a77391d2ae4afc7fac3304bfb3))

* Merge pull request #941 from pirate486743186/edit-readme

[minor]clarifying youtube-dl usage in readme ([`b774b85`](https://github.com/mps-youtube/yewtube/commit/b774b851424d27c81ae432d3217c1afc7fab70f8))

* clarifying youtube-dl usage in readme ([`33df500`](https://github.com/mps-youtube/yewtube/commit/33df50091974084ef498b60e742e54ad97c873a8))

* Merge pull request #943 from vikramkashyap/readme_code_fix

Fix README Linux install instruction formatting ([`906f27f`](https://github.com/mps-youtube/yewtube/commit/906f27f27447c4170c71d09fb744571a79a99c33))

* Fixed linux install instructions formatting ([`41b66d8`](https://github.com/mps-youtube/yewtube/commit/41b66d8e42f6b9808dfb179aa2387562866246b3))

* Merge pull request #954 from pirate486743186/min-resolution

[minor] increasing minimum resolution to 360 from 192 ([`7c36bc9`](https://github.com/mps-youtube/yewtube/commit/7c36bc952ff41dba0a5836760d6e8b97c006ab47))

* increasing minimum resolution to 360 ([`9c40cc0`](https://github.com/mps-youtube/yewtube/commit/9c40cc071e47f5fff6957f33a06d1751e3ab6471))

* Merge pull request #931 from vikramkashyap/develop

Fix help text altering the terminal color ([`881dfe7`](https://github.com/mps-youtube/yewtube/commit/881dfe74a67ad6c2c6b3be480557d8894d330973))

* Remove stray color flag in helptext ([`ccab53b`](https://github.com/mps-youtube/yewtube/commit/ccab53b5f0a2779a7d7935bbb81402a3094334a0))

* Merge pull request #963 from lopsided98/playlist-prefixes

Synchronize playlist prefixes with pafy ([`91104b0`](https://github.com/mps-youtube/yewtube/commit/91104b0113e9f0acaa81e7770b8872a58cd7c449))

* Synchronize playlist prefixes with pafy. ([`dc51497`](https://github.com/mps-youtube/yewtube/commit/dc514973497cad306c2bd1130415966c00dc97eb))

* Merge pull request #959 from azisyus/develop

always_repeat mode added which is configurable via &#34;set always_repeat true|false&#34; ([`7ced7ff`](https://github.com/mps-youtube/yewtube/commit/7ced7ff08c364fe355ec4ccac18a0071ec187efe))

* Update config.py ([`7aee0da`](https://github.com/mps-youtube/yewtube/commit/7aee0daec0f5d94967283072fbabdf10a9a3659a))

* always_repeat mode added which is configurable via &#34;set always_repeat true|false&#34; ([`bf8e57b`](https://github.com/mps-youtube/yewtube/commit/bf8e57bc5e9a7bee5f13aa96b42b60d344bee161))

* Handle OLxxx playlists

It appears some playlist IDs may start with OL:

https://www.youtube.com/watch?v=nrvMe70ANuA&amp;list=OLAK5uy_lakUEV0QpMEe8mXcx_v6yrZkwXzTleayk ([`0d21ac3`](https://github.com/mps-youtube/yewtube/commit/0d21ac37fe9f676b4cfb21a2f12e982baa770b3c))

* Merge pull request #936 from willhallonline/develop

Dockerfile improvements ([`7be7628`](https://github.com/mps-youtube/yewtube/commit/7be7628bd6770ec23e73da181a372119eae6d782))

* 1. Drop Maintainer (deprecated)
2. Add layers for better understanding of container build
3. Reduce layer use for easier caching. ([`e2d9a22`](https://github.com/mps-youtube/yewtube/commit/e2d9a22c6b19e7dc31551cb3eea3d0c93cd5ee58))

* Merge pull request #890 from nishanthkarthik/develop

Refactor create_playlist to remove unnecessary branch ([`00f9c9b`](https://github.com/mps-youtube/yewtube/commit/00f9c9be9cd7a6875df90911b096a458d6542a99))

* Refactor create_playlist to remove unnecessary branch ([`8776f64`](https://github.com/mps-youtube/yewtube/commit/8776f64eab8901bdc24d43b00f9488ee3c227411))

* Merge pull request #892 from andreparames/qrcode

[Suggestion] Show QRCode in video information panel ([`18a12ba`](https://github.com/mps-youtube/yewtube/commit/18a12bad987ebbccdeeaa27065608e243b686a9f))

* Show QRCode in video information panel

Uses the qrcode library to print an ASCII qrcode of the URL of
the video, if the new option `show_qrcode` is enabled. ([`01cd91b`](https://github.com/mps-youtube/yewtube/commit/01cd91b2e3990f7e7e2507471298d5d31ef87948))

* Merge pull request #882 from hrnr/mpris_yturl

export youtube URL in MPRIS metadata ([`ed812e7`](https://github.com/mps-youtube/yewtube/commit/ed812e75cbff378732a353111a80d2ad4d574358))

* export youtube URL in MPRIS metadata

* fixes #881
* use xesam:url to export youtube url ([`7887017`](https://github.com/mps-youtube/yewtube/commit/7887017c564b88973ee11949691a7830d9099e6f))

* Merge pull request #875 from murnux/develop

Add Arch Linux install instructions ([`eb9e500`](https://github.com/mps-youtube/yewtube/commit/eb9e5004728368a03dfd5a92ae94fb53895360e8))

* Add Arch Linux install instructions

Similar to Ubuntu, add terminal command to install from the Arch Linux official repos. ([`af6adee`](https://github.com/mps-youtube/yewtube/commit/af6adee8bb450d5d1e4d7161f51b2082258773f0))

* Merge pull request #873 from RivkaDedic/patch-1

Extended OSX installation instructions ([`a3882fe`](https://github.com/mps-youtube/yewtube/commit/a3882fed06c4d5c76c9ecfbe99d714732fdfe173))

* Extended OSX installation instructions

Added actual mps-youtube installation command ([`22bcea1`](https://github.com/mps-youtube/yewtube/commit/22bcea16cde2a281d424202246ac17b48a04b18e))

* Merge pull request #871 from mevCJ/develop

Changed CONTRIBUTING to markdown format; added new section in readme ([`4d18843`](https://github.com/mps-youtube/yewtube/commit/4d18843df24ee464216e2973a19fafc6e91cab93))

* Update README.rst

&#39;How to contribute&#39; section is added. ([`2789a6e`](https://github.com/mps-youtube/yewtube/commit/2789a6e248d2ac1e703a18a8d7a249baa5cc66e2))

* Update and rename CONTRIBUTING to CONTRIBUTING.md

Changed CONTRIBUTING to markdown format to make reading easier. ([`08e7e47`](https://github.com/mps-youtube/yewtube/commit/08e7e47df3fb18de6cf7905c727bb14d19b8e9b8))

* Merge pull request #852 from Laxa/develop

Fix #847 =&gt; Player crash when video is unavailable or forbidden ([`4279caa`](https://github.com/mps-youtube/yewtube/commit/4279caa5f343aa6ad14a2d550d1c65d1d745f4dc))

* Fix #847 ([`79ac6ea`](https://github.com/mps-youtube/yewtube/commit/79ac6ea8521b85788d130cf174c9f6878d2225cd))

* Merge pull request #858 from Razesdark/disabled_comments_fix

Filter out html code from pafy.util.GdataError ([`3bf9e34`](https://github.com/mps-youtube/yewtube/commit/3bf9e344ddc4214eeef4ca27b9ea66dc23e28cf7))

* Remove line blank in fetch_comments ([`5431333`](https://github.com/mps-youtube/yewtube/commit/5431333ced0f6280c16c09939dd5b8e782b02bbe))

* Throw error instead of print ([`d8165fd`](https://github.com/mps-youtube/yewtube/commit/d8165fd4873e205b953e15ebba1a021d628ce029))

* Filter out code from pafy.util.GdataError

References #820

pafys GDataError uses error messages from returned
api calls.

If comments were called on a video with comments disabled;
the error returned would be somewhat non-sensical to an
end user.

The error message contained some superflous information including
the html code pasted below.
`&lt;code&gt;&lt;a
href=\&#34;/youtube/v3/docs/commentThreads/list#videoId\&#34;&gt;videoId&lt;/a&gt;&lt;/code&gt;`

This commit removes the superflous information and
has the function return a simple `Youtube error 403: The video has
comments disabled&#34; ([`1ed2916`](https://github.com/mps-youtube/yewtube/commit/1ed2916bf87711ab16884597e6ad957263d31112))

* Merge pull request #867 from Razesdark/hotfix/encrypt_and_optout_lastfm_metadata_793

Use https and add optout for metadata via last.fm ([`b90ba12`](https://github.com/mps-youtube/yewtube/commit/b90ba12b81b069020917db342f2155a4f851a165))

* Style change ([`b967a45`](https://github.com/mps-youtube/yewtube/commit/b967a45ebe9678d6f1f9d9daec8b21220f174ecf))

* Check for optout on call instead of in function ([`94e9cb4`](https://github.com/mps-youtube/yewtube/commit/94e9cb41a365ca3d477370c179eaebfb9283a9e3))

* Add helptext for lookup_metadata option ([`c2a670b`](https://github.com/mps-youtube/yewtube/commit/c2a670bcd8c2df9e8e199d12e9cbaa41deaf9f30))

* Use https over http ([`a0dc4a8`](https://github.com/mps-youtube/yewtube/commit/a0dc4a804b9db9a279a60a648c028720dc22befb))

* Add option to skip metadata ([`cee37b0`](https://github.com/mps-youtube/yewtube/commit/cee37b00857667913196db916b060fe8eb3dace0))

* Merge pull request #866 from Razesdark/hotfix/category_denied_864

Let lastfm metadata recover on HTTPError ([`d68fe0f`](https://github.com/mps-youtube/yewtube/commit/d68fe0f0044f296d712e0f84a9744e63866fd103))

* Squash except statements ([`fc8f79f`](https://github.com/mps-youtube/yewtube/commit/fc8f79f3af4307eddb17f6f90b40bf6bd5f89167))

* Also allow metadata_lastfm to recover when api is unreachable

Signed-off-by: Tommy Stigen Olsen &lt;tommsolsen@gmail.com&gt; ([`b495255`](https://github.com/mps-youtube/yewtube/commit/b49525578b0ca2317f756868616d7fe0cb94e3f5))

* Have get_metadata_from_lastfm respond to HTTPErrors

If loading the data fails for some reason, have the software return none and continue instead of throwing errors. ([`7fa2cfd`](https://github.com/mps-youtube/yewtube/commit/7fa2cfdd94d11d2e6d855a5c7acea07522687325))

* Merge pull request #863 from ferrybig/patch-1

Fix broken url&#39;s in readme ([`394860f`](https://github.com/mps-youtube/yewtube/commit/394860fe24bc42f7b8da227e94a97f724c61a72e))

* Fix broken url&#39;s in readme

Still broken without me finding proper replacements:

* https://github.com/np1/mps ([`13dd575`](https://github.com/mps-youtube/yewtube/commit/13dd57594fc270a27c6af22a3422aefc9f5a6e5d))

* Merge pull request #862 from cclauss/patch-1

Capture the raised exception ([`f108f06`](https://github.com/mps-youtube/yewtube/commit/f108f06364906828b4a92e479ef54afd5dd2ec8d))

* Capture the raised exception for error reporting

Capture the raised exception in the variable __e__ on line 39 so that it can be recorded on line 41.

flake8 testing of https://github.com/mps-youtube/mps-youtube on Python 3.6.3

$ __flake8 . --count --select=E901,E999,F821,F822,F823 --show-source --statistics__
```
./mps_youtube/commands/lastfm.py:41:63: F821 undefined name &#39;e&#39;
            g.message = &#34;Last.fm connection error: %s&#34; % (str(e))
                                                              ^
1     F821 undefined name &#39;e&#39;
1
``` ([`67ece36`](https://github.com/mps-youtube/yewtube/commit/67ece36dcddeaf2aedb426c078fb98515547d99b))

* Merge pull request #859 from Razesdark/better_commands

Better @command definition that can register tab-completion strings ([`5fd76ae`](https://github.com/mps-youtube/yewtube/commit/5fd76ae7d3b44a8d760ee0105fb9b29ffb326272))

* Remove more debug code ([`9ae5b2f`](https://github.com/mps-youtube/yewtube/commit/9ae5b2f44de54355e8b8775e4d28e817b43ac77a))

* update documentation ([`0637e75`](https://github.com/mps-youtube/yewtube/commit/0637e751f9ae39e975df923837a70628ad1bc6c2))

* Merge branch &#39;better_commands&#39; of github.com:Razesdark/mps-youtube into better_commands ([`9b878bb`](https://github.com/mps-youtube/yewtube/commit/9b878bb88b0364cd44ceba48a4213038f64d21b4))

* Remove debug messages ([`f70a352`](https://github.com/mps-youtube/yewtube/commit/f70a352be670a69b63643b133e0cca665d04a001))

* Remove unrelate changes ([`73838c0`](https://github.com/mps-youtube/yewtube/commit/73838c09aecb0435327031ae63a87c87f853033f))

* Add documentation for new @command ([`b68dbb5`](https://github.com/mps-youtube/yewtube/commit/b68dbb54a64e6548f6b67dcd82c3e71e0f38647c))

* Move tab-completion command definitions &gt; @command

Instead of having a predefined list of commands in util,
the commands are appended to the list from the @command
function. ([`38e7389`](https://github.com/mps-youtube/yewtube/commit/38e7389f4961aca216a8ca12ca1ff9078ed6a022))

* Merge pull request #855 from mps-youtube/no-fstrings

No fstrings allowed ([`ac58452`](https://github.com/mps-youtube/yewtube/commit/ac58452430d6518b9fc10417e627fa18fe537739))

* No fstrings allowed ([`e0e1c56`](https://github.com/mps-youtube/yewtube/commit/e0e1c568734719387ab327eecaba6a383212bf57))

* Merge pull request #848 from BlackCapCoder/patch-1

Added `set -t` to the help text ([`9000a1a`](https://github.com/mps-youtube/yewtube/commit/9000a1a79ac9d10e06dd4fff81e24e4efeded563))

* Fixed colors

I assumed `{1}` and `{2}` was for formatting and only tested it with `mpsty --help | less`. ([`77436c3`](https://github.com/mps-youtube/yewtube/commit/77436c3719e9e041ff2fabd04261de35beb73a8a))

* Added `set -t` to the help text ([`ed64641`](https://github.com/mps-youtube/yewtube/commit/ed646418f6cc26517c6fd9287e1be503ce960292))

* Merge pull request #803 from BlackCapCoder/tempset

Implemented temporary settings option `set -t` ([`ad01e66`](https://github.com/mps-youtube/yewtube/commit/ad01e66fdb1bf6f3b15adeb835d05c21260e9fc8))

* implemented set -t ([`319f0ca`](https://github.com/mps-youtube/yewtube/commit/319f0cab904a68992b52dc8ce483f7e124c94d2f))

* implemented auto_save_settings setting ([`d859dba`](https://github.com/mps-youtube/yewtube/commit/d859dba93f9d03491b822348d1094ddcfd200c9c))

* fixed #455 ([`ca5393d`](https://github.com/mps-youtube/yewtube/commit/ca5393dbf62263a37e898d97b2c0748d35a9971e))

* Merge pull request #846 from Razesdark/new-image-mpsyt

Update readme with new urls ([`d3952ee`](https://github.com/mps-youtube/yewtube/commit/d3952ee8870a334e814a19ee9f6ccd980e0d2019))

* Update readme with new urls ([`7405962`](https://github.com/mps-youtube/yewtube/commit/74059629153fc0f544d8e6a6c58c52634ecfed8a))

* Fix mpris crash on KeyboardInterrupt ([`0100a38`](https://github.com/mps-youtube/yewtube/commit/0100a38d3874c53e705d9acd7e30fbc6a3099da0))

* Merge pull request #833 from ritiek/fix-duration

Show values greater than 24 hours correctly ([`9771d33`](https://github.com/mps-youtube/yewtube/commit/9771d33d390dd6550f82bba16df4871d590071c3))

* Show values greater than 24 hours correctly ([`2ad3c11`](https://github.com/mps-youtube/yewtube/commit/2ad3c1197726be034f71426f9d559d237997dc34))

* Merge pull request #805 from ritiek/fetch-private-playlists

Fetch private playlists when using direct spotify link ([`18fa860`](https://github.com/mps-youtube/yewtube/commit/18fa860f7517099634c453a5b4be3cf15b268e93))

* Fetch private playlists when using direct spotify link ([`bede09f`](https://github.com/mps-youtube/yewtube/commit/bede09f1def23bbc8584c9f9ae9d333b08b42d10))

* Merge pull request #789 from vn-ki/tab-completion

Add tab completion for in program commands ([`146df59`](https://github.com/mps-youtube/yewtube/commit/146df5970a8968634f904aa3c3f73a847846ed34))

* Get SET_COMMANDS from config ([`a87e2f8`](https://github.com/mps-youtube/yewtube/commit/a87e2f86b8f20d090e0e7b74917b8f37b531118e))

* Extend autocomplete to set variables ([`32fdf77`](https://github.com/mps-youtube/yewtube/commit/32fdf771263c5115635aeb47b0f6c3813ba98ad7))

* Add tab completion for in program commands ([`5b1c77f`](https://github.com/mps-youtube/yewtube/commit/5b1c77f2f9b3e4992465364c7fdf993065122d1d))

* Merge pull request #791 from dragosprju/patch-1

Fix &#39;mkp&#39; when used with a text file ([`91ccf41`](https://github.com/mps-youtube/yewtube/commit/91ccf41dd5194beaff847beb33ea41ec8c228203))

* Fix &#39;mkp&#39; when used with a text file

If we call .replace on `title` and `title` is None from the get-go, as it is defined as such in the parameter list, then the command `mkp` inside the program crashes the program. `help search` in the program never suggests to have a title for the playlist as argument for `mkp`. From where `create_playlist` function is called (inside `generate_playlist` function), it never receives an argument for `title`, as such `title` remains None and gets called with .replace (and crashes program). Therefore, `mkp list.txt` for example will always crash the program when trying to make a playlist based off a text file.

This code could be made more shorter, but I don&#39;t write Python much. It is also my first ever pull request so bear with my beginner tendencies. ([`fef24ab`](https://github.com/mps-youtube/yewtube/commit/fef24ab6b0cb9030b823ac1fe4691b0b5dcf6869))

* resp.read().decode(..), not resp.decode(..) ([`d0a3eee`](https://github.com/mps-youtube/yewtube/commit/d0a3eee3962596dd3ef1f26d7b5f2f2ed812f6a4))

* Add note about --user and PATH ([`43f811e`](https://github.com/mps-youtube/yewtube/commit/43f811eef6322fced13a3437be0849795a3a5016))

* Merge remote-tracking branch &#39;orschiro/patch-2&#39; into develop ([`efc1b14`](https://github.com/mps-youtube/yewtube/commit/efc1b143100d1c29ad8b6a3c525bb0fd66a568fa))

* Add pip3 --user flag and remove sudo ([`2aa8bc1`](https://github.com/mps-youtube/yewtube/commit/2aa8bc1c31c435f5ea6eb9611c6a26e146f3e28d))

* Prior to Python 3.6, json.loads cannot take a bytes object ([`e215364`](https://github.com/mps-youtube/yewtube/commit/e2153640531c29a515ab17b4073a300f80093f30))

* Remove unneeded if condition

try/except should handle this ([`dfffb3a`](https://github.com/mps-youtube/yewtube/commit/dfffb3a343f733779cb3dc27bc8d4a1fa3fc457e))

* Change json.loads to json.load ([`7b3026a`](https://github.com/mps-youtube/yewtube/commit/7b3026a67e7f25cd411fbf48e45b5e43a70f184e))

* Switch from bare except to IndexError and KeyError ([`a97c234`](https://github.com/mps-youtube/yewtube/commit/a97c234c20aba0ebeaab3cad1b33a964696a0aa3))

* Fix json error in some python distributions

Change respone.read() to response.read().decode(&#39;utf-8&#39;) ([`aef45ae`](https://github.com/mps-youtube/yewtube/commit/aef45ae68f13d6179aa3831eee58466901875495))

* Change setup.py to include mps_youtube.players ([`9cc924c`](https://github.com/mps-youtube/yewtube/commit/9cc924c78c938306da7b0c58cab3b99d56703157))

* str.spit -&gt; str.split ([`5cdbf52`](https://github.com/mps-youtube/yewtube/commit/5cdbf52143a59332a1020827d14a9f02bb37ecff))

* CHANGELOG: fix git log command ([`6181200`](https://github.com/mps-youtube/yewtube/commit/6181200b270515fcafa2f42eb3dbae72976083b2))

* Merge pull request #753 from vn-ki/refactor-player

Refactor player.py ([`d1a006f`](https://github.com/mps-youtube/yewtube/commit/d1a006fdb5a73f284e10ee41731b9c418f127156))

* Wrap _make_status_line in another func. ([`824f530`](https://github.com/mps-youtube/yewtube/commit/824f530bb52b95ec834ec58ee6a71a7459dc80a1))

* Make the requested changes

Fixed not loading of player when using path or .exe.
Renamed generic_player to GenericPlayer
Moved default args of mpv and mplayer to player class.
Assign g.PLAYER_OBJ during set player command. ([`ecd80da`](https://github.com/mps-youtube/yewtube/commit/ecd80dab906aee024514b8c81e9ed7b01e43d65f))

* Make BasePlayer more abstract ([`88fd76d`](https://github.com/mps-youtube/yewtube/commit/88fd76d296f533cbc73539e758e38b792c68088f))

* Merge branch &#39;develop&#39; into refactor-player ([`a9d7675`](https://github.com/mps-youtube/yewtube/commit/a9d7675c44de601cd370c5e48f74750db5030ad3))

* Changes to facilitate use of player library ([`6988874`](https://github.com/mps-youtube/yewtube/commit/6988874dd8a63e71a38bb01f697f17a45266676b))

* Implement dynamic import for players ([`8ee09a7`](https://github.com/mps-youtube/yewtube/commit/8ee09a7fe1162200fbda330e9614649350bd2cd1))

* Minor fixes ([`b50f788`](https://github.com/mps-youtube/yewtube/commit/b50f7887d61179bdfe2aa3148e3c645e723f0ab2))

* Add vlc and generic_player ([`914b9e1`](https://github.com/mps-youtube/yewtube/commit/914b9e12337be71f7db22671366052d455e86654))

* Add support for mplayer ([`2ce0611`](https://github.com/mps-youtube/yewtube/commit/2ce061189dd262716fc1268189e76b115d11b817))

* Revert back to old mpris.py ([`47f6136`](https://github.com/mps-youtube/yewtube/commit/47f61369b86cc104808ab6e4de3d01dedb792f8b))

* Partial fix mpris,py ([`8703a8c`](https://github.com/mps-youtube/yewtube/commit/8703a8c9e14b8e87924b563ca81d111d543620ee))

* Remove old player.py ([`ecc70c6`](https://github.com/mps-youtube/yewtube/commit/ecc70c658f652740a9db79f61aa0ecca78c808e1))

* Implement interface for mpv player ([`973741d`](https://github.com/mps-youtube/yewtube/commit/973741d2e04c55c561d55809c2d08746756bcd01))

* Primary draft ([`12498b2`](https://github.com/mps-youtube/yewtube/commit/12498b20ff89bd2682a7f0915cbde5911a37e9af))

## v0.2.8 (2018-02-17)

### Unknown

* Version 0.2.8 ([`da798cf`](https://github.com/mps-youtube/yewtube/commit/da798cf4f80513ebb424257e3fed9e9dd72c980b))

* Merge pull request #772 from SanketDG/fix-unique-history

history: Fix recent subcommand hiding duplicates ([`bfe9326`](https://github.com/mps-youtube/yewtube/commit/bfe9326b934d5c9ed4c7ed3f528a8c08e25a1213))

* history: Fix recent subcommand hiding duplicates ([`c7bde20`](https://github.com/mps-youtube/yewtube/commit/c7bde20395955045d29ef485b3d7db663fb2fbae))

* Merge pull request #758 from rien333/develop

Added Last.fm support ([`6d9b45c`](https://github.com/mps-youtube/yewtube/commit/6d9b45c218d69fe3c52d00a8e82f2e2965585f18))

* Silence an inappropriate warning ([`8eebd0c`](https://github.com/mps-youtube/yewtube/commit/8eebd0c927781912bc20be9eac8c1c6f401dc2f4))

* Scrobble album title information ([`6fe9214`](https://github.com/mps-youtube/yewtube/commit/6fe921497c03e7e041d4e1542b2c92566fc90fbd))

* whitespace correction ([`02969fd`](https://github.com/mps-youtube/yewtube/commit/02969fdbf4b95e2a6631269cbfeba96676545b83))

* Added Last.fm support ([`1137b3c`](https://github.com/mps-youtube/yewtube/commit/1137b3c1f67ff01f408194170f6677cd84ea4eaa))

* Revert &#34;Allow more than 500 results for searches&#34;

This reverts commit e378dbcfd99f6188b82679769bcc662c5e0be879.

According to the docs:

&#34;Note: Search results are constrained to a maximum of 500 videos if your
request specifies a value for the channelId parameter and sets the type
parameter value to video, but it does not also set one of the
forContentOwner, forDeveloper, or forMine filters.&#34;

https://developers.google.com/youtube/v3/docs/search/list

The number of results returned does, however, seem limited for a normal
search as well, and not entirely consistently. If possible, this should
be fixed, but I don&#39;t know what is going on. ([`0e6d180`](https://github.com/mps-youtube/yewtube/commit/0e6d1803f9d764cad5945443deee211b2e677749))

* Allow more than 500 results for searches ([`e378dbc`](https://github.com/mps-youtube/yewtube/commit/e378dbcfd99f6188b82679769bcc662c5e0be879))

* Merge pull request #748 from Laxa/develop

Player_status: minutes are now correctly displayed ([`949f984`](https://github.com/mps-youtube/yewtube/commit/949f984aed56fb7c41732897eae5c3ddc80df00d))

* Player_status: minutes are now correctly displayed ([`c1d746f`](https://github.com/mps-youtube/yewtube/commit/c1d746f951ebcd9869ed5a0352f7653b851018a5))

* Minor fixes ([`8a55803`](https://github.com/mps-youtube/yewtube/commit/8a558030fbfc05fbb647206212729964ce602f73))

* Added doc strings ([`eedde53`](https://github.com/mps-youtube/yewtube/commit/eedde5320f640905868c7f1f8d5b014f36a95df7))

* Show proper metadata including album and artist whenever possible ([`46f6568`](https://github.com/mps-youtube/yewtube/commit/46f65683ad13b83974c5a3598c19990ede6cb9a0))

* Merge remote-tracking branch &#39;razesdark/patch-2&#39; into develop ([`8cf7c73`](https://github.com/mps-youtube/yewtube/commit/8cf7c7313b494852b10f0f5cd13fdf5307150a3c))

* Update ISSUE_TEMPLATE.md ([`f50b7e0`](https://github.com/mps-youtube/yewtube/commit/f50b7e068b31a67629ad3ccdb09dea5b78915cc7))

* Update ISSUE_TEMPLATE.md

We seem to be getting predominantly issues where we end up having to ask for the same information; mpsyt version, youtube-dl version etc.

I suggest we add a issue template in an effort to try to raise quality of incoming issues. ([`e2c5923`](https://github.com/mps-youtube/yewtube/commit/e2c59230db32047c43914330578b892727d8d645))

* Merge remote-tracking branch &#39;orschiro/patch-2&#39; into develop ([`9ca0909`](https://github.com/mps-youtube/yewtube/commit/9ca09094ae5257523256ac34f8df63186329d59f))

* Added IRC link to join directly ([`d2e8fe4`](https://github.com/mps-youtube/yewtube/commit/d2e8fe4e26edac0d6840648c3452ac53ceceadfb))

* Merge remote-tracking branch &#39;ritiek/skip-unavailable&#39; into develop ([`685f298`](https://github.com/mps-youtube/yewtube/commit/685f298f2bc47219772787f024603bc41948b9b7))

* Skip unavailable tracks ([`88e0ecb`](https://github.com/mps-youtube/yewtube/commit/88e0ecb8b82f146e21a26f7172d5e5dc5f14f87f))

* Merge remote-tracking branch &#39;oxij/fix-channel-search&#39; into develop ([`0ed54dd`](https://github.com/mps-youtube/yewtube/commit/0ed54ddaae30cc7e1d610e3bd8d2db684fe3d816))

* fix &#34;channels&#34; command ([`135bba9`](https://github.com/mps-youtube/yewtube/commit/135bba9cbb5612448f076ae511688203b8c258d4))

* Merge remote-tracking branch &#39;razesdark/repeat_volume_fix&#39; into develop ([`192e59f`](https://github.com/mps-youtube/yewtube/commit/192e59fdc9d4098b91802308518e594f9278e116))

* Remove debug print statement

Signed-off-by: Tommy Stigen Olsen &lt;tommysolsen@gmail.com&gt; ([`7b24d6e`](https://github.com/mps-youtube/yewtube/commit/7b24d6eab92e5a438033ef55af174b0c22e28ae0))

* Adds mplayer volume control

Volume control for mplayer

Signed-off-by: Tommy Stigen Olsen &lt;tommysolsen@gmail.com&gt; ([`1b483d2`](https://github.com/mps-youtube/yewtube/commit/1b483d29f7040b697f99307f953314106748470f))

* Store volume for later use

Signed-off-by: Tommy Stigen Olsen &lt;tommysolsen@gmail.com&gt; ([`53c90bc`](https://github.com/mps-youtube/yewtube/commit/53c90bcd629647199f5046ff9fcadd6302d7d47d))

* Merge pull request #728 from hrnr/mpris_fixes

MPRIS fixes ([`29538b0`](https://github.com/mps-youtube/yewtube/commit/29538b0b0aec3e5a1e2e40d965b4973cf8770061))

* never crash main process when MPRIS process fails

* increased MPRIS failure logging to make it easier to debug for users. If annoying MPRIS can now be disabled with `set mpris 0`
* fixes #706 ([`14684bd`](https://github.com/mps-youtube/yewtube/commit/14684bd9306056c929e8194c2cfe02d1b7ffa8fa))

* mpris: allow to disable MPRIS interface

* new config option to disable MPRIS process at all
* fixes #408 ([`0f9b10d`](https://github.com/mps-youtube/yewtube/commit/0f9b10daccfd5b3b474222b042cd46a6dd614fd0))

* Merge pull request #717 from orschiro/patch-3

Dev installation and Ubuntu ([`64b4185`](https://github.com/mps-youtube/yewtube/commit/64b4185aa6eaecaa0ff29ed82d6e331b7366e86d))

* Dev installation and Ubuntu ([`75d8658`](https://github.com/mps-youtube/yewtube/commit/75d8658ef7f24d1a0f108fd625d904b1ba194c64))

* Merge pull request #702 from sheshang/readme-update-branch

updated youtube-dl notation ([`a51a9d7`](https://github.com/mps-youtube/yewtube/commit/a51a9d7a77ce44fd276309d52b2fbe0abf95a86d))

* updated youtube-dl notation

here youtube-dl was referred as youtube_dl buit it is wrong. It will give error. So actually you should write as youtube-dl ([`0912985`](https://github.com/mps-youtube/yewtube/commit/091298519a75a5c510c1dcde41087a3aedd38e80))

* Merge pull request #695 from kraetzin/rm-fix

Fix rm command to correctly remove song from playlist ([`b55a8e6`](https://github.com/mps-youtube/yewtube/commit/b55a8e6972af2ef82411d99d2eed42fcf5a64c8e))

* Fix invalid item range error for  on search results ([`a4f37d3`](https://github.com/mps-youtube/yewtube/commit/a4f37d3a8a0cbbc9cba8846a883a3a60e7616bad))

* Fix rm command to correctly remove song from playlist, preserved between page changes ([`a4e8730`](https://github.com/mps-youtube/yewtube/commit/a4e87301c2277580ccfccc1fafb7c7fb904c3ac0))

* Merge pull request #691 from Vrihub/download_unsorted

Allow da/dv with unsorted items (fix #554) ([`8ec34b1`](https://github.com/mps-youtube/yewtube/commit/8ec34b1398e77a27208b19d66e04b94a988517c3))

* Allow da/dv with unsorted items (fix #554)

Fix the regexp for the da/dv commands to download multiple items,
allowing items list to have any number of digits (i.e. what we
initially called &#34;unsorted&#34; items in issue #554).

Fix issue #554 and the regression contained in the solution proposed
in commit 11765660293f356878bc7fb8fbbc5f88582a4d20 ([`cf092a7`](https://github.com/mps-youtube/yewtube/commit/cf092a7684747df6cced8a7e0482f5782a5c76b3))

* Merge pull request #687 from mg6/mpv-abs-seek

Fix absolute seek through MPRIS with mpv v0.24.0 ([`acbbcd2`](https://github.com/mps-youtube/yewtube/commit/acbbcd224478f9b350a70bfad41e3ecf51d66ad1))

* Fix absolute seek through MPRIS with mpv

When using an MPRIS-compatible playback widget under GNOME, the
following error appears as the user sets absolute track position:

  [ipc_0] Command seek: argument 2 has incompatible type.

As it turns out, mpv v0.24.0 expects seek mode argument to be a string.
The string seek mode parameter is supported since mpv v0.1.0. ([`c484c51`](https://github.com/mps-youtube/yewtube/commit/c484c51e203d1c7abaaaa9d7f4953a143411d196))

* Merge pull request #684 from ritiek/develop

Do not clear songlist after playback ([`97b9151`](https://github.com/mps-youtube/yewtube/commit/97b91518d01f0b56bc2ed9b457a5cbd103509872))

* Do not clear songlist after playback ([`6d1788c`](https://github.com/mps-youtube/yewtube/commit/6d1788c2a7ba3a5e960a462e446e400098af5f0f))

* Merge pull request #682 from kraetzin/m3u

Use m3u files for playlists ([`3768fa9`](https://github.com/mps-youtube/yewtube/commit/3768fa92c8f40096c762292569d41639232f6d7f))

* Add os.mkdir() in conversion exception handling ([`f2bfb60`](https://github.com/mps-youtube/yewtube/commit/f2bfb60f6fba13c310316ad1994dd862e9a37692))

* Strip newline from ytid to prevent newline for every mpv status update. ([`a7c3b5b`](https://github.com/mps-youtube/yewtube/commit/a7c3b5b0033f2682eebe62553ea296f5bb9d91cc))

* Remove useless line ([`2d7d911`](https://github.com/mps-youtube/yewtube/commit/2d7d911b92a6266a865b5f7106900f2113729832))

* Remove underscore from read_m3u() ([`11bb5ea`](https://github.com/mps-youtube/yewtube/commit/11bb5ea26ea81467339632fc8645c411dc81ddc4))

* Switch play history to use m3u format. ([`f5293c3`](https://github.com/mps-youtube/yewtube/commit/f5293c3e6f6c885e9a11deadebd51f3b908f2dec))

* Re-add removed exceptions to _convert_playlist_to_m3u() conversion instead of load() ([`e2f51e0`](https://github.com/mps-youtube/yewtube/commit/e2f51e0cc92360a8afdaf8c4fc1f92df416e7157))

* Remove commented exceptions that shouldn&#39;t apply anymore. ([`5f7286f`](https://github.com/mps-youtube/yewtube/commit/5f7286ffa1b8763b430e52ea597b1e16a94568a0))

* Fix rmp command so it removes m3u file. ([`51c504b`](https://github.com/mps-youtube/yewtube/commit/51c504b29a4ffc0db4e834a32fd205ab643523dd))

* Use pafy to extract ytid ([`09c8e17`](https://github.com/mps-youtube/yewtube/commit/09c8e17ec9f675f949b1da4c6e05b4f7454d11e2))

* Add handling of basic m3u list of urls ([`ab7f793`](https://github.com/mps-youtube/yewtube/commit/ab7f7938f80ea7944a6e6eeaa0e8588d73b32a4f))

* Remove print statement ([`7ea38f2`](https://github.com/mps-youtube/yewtube/commit/7ea38f25f57593a1d7346dd1d666bfade974ae39))

* Implement loading of #EXTM3U playlist files. ([`b47520d`](https://github.com/mps-youtube/yewtube/commit/b47520d04aee1ee4a7534a3813e27ecd5bbbe89f))

* Begin changing of load() to read m3u files. ([`fa32db5`](https://github.com/mps-youtube/yewtube/commit/fa32db538858c60b796a17af077425659a49d221))

* Change save() function to use m3u ([`fa862cc`](https://github.com/mps-youtube/yewtube/commit/fa862cca6f69387397081e966bbf4a148bb89632))

* Convert old playlist file to multiple m3u files ([`0e7bc1f`](https://github.com/mps-youtube/yewtube/commit/0e7bc1fc1560badb7a3e570412c7677c6f432858))

* Fix splaylist and suser with no argument ([`6b03b67`](https://github.com/mps-youtube/yewtube/commit/6b03b67685165790a5fb238d82a16421cf81458a))

* Merge remote-tracking branch &#39;ritiek/spotify&#39; into develop ([`ba6a2d2`](https://github.com/mps-youtube/yewtube/commit/ba6a2d2ba08d080c01b0c8ce5bfbe237ddf1bfdd))

* spotipy as optional dependency ([`223950c`](https://github.com/mps-youtube/yewtube/commit/223950c5e893d371e9272c09ac84011da09ac013))

* spotipy as optional dependency ([`c97c263`](https://github.com/mps-youtube/yewtube/commit/c97c263caae213532532a3a0e5a159ff398bed26))

* Add spotipy as a requirement ([`48a0502`](https://github.com/mps-youtube/yewtube/commit/48a0502fb260a99dd2fcdfa799654438ac9b151e))

* Add spotipy as a requirement ([`b209782`](https://github.com/mps-youtube/yewtube/commit/b2097825d64f67b8acea3a640cd467300327c789))

* Generate new public keys ([`71ea1fc`](https://github.com/mps-youtube/yewtube/commit/71ea1fc0e65e5c85ff611e513dd90c2534854a26))

* Remove unused code ([`256a431`](https://github.com/mps-youtube/yewtube/commit/256a431ca69724865c26d7badc364e3b69234c10))

* Some cleaning ([`5f4a991`](https://github.com/mps-youtube/yewtube/commit/5f4a9911f456696ad1f9329c9d881992f69c17d2))

* Match tracks and fix imports ([`159efff`](https://github.com/mps-youtube/yewtube/commit/159efffe91e7d3169b46127e2e579f95f3dedbc1))

* Show playlist tracks ([`1bd6f32`](https://github.com/mps-youtube/yewtube/commit/1bd6f32faa341cf3e72149869e418a0de3f34066))

* Fetch spotify track info ([`8d6ef40`](https://github.com/mps-youtube/yewtube/commit/8d6ef40a2f8d926601e82c343fed071e850054a9))

* Add splaylist command to fetch Spotify playlist ([`25886a4`](https://github.com/mps-youtube/yewtube/commit/25886a41f429b0c6447bdb062093bbf69ae2a6a3))

* Merge pull request #675 from ritiek/develop

Show stream details in video information ([`531e6b9`](https://github.com/mps-youtube/yewtube/commit/531e6b96b35d0d625ff72a5e123226046b5cd3d0))

* Test for player only when actually playing ([`fd7c858`](https://github.com/mps-youtube/yewtube/commit/fd7c8582433b0af9379b9eddc49142d1d6828104))

* Fix conflicting function names ([`51e8e67`](https://github.com/mps-youtube/yewtube/commit/51e8e67e5c581a2fef4668292895986958706cb2))

* Add s command to fetch stream information ([`9a8893d`](https://github.com/mps-youtube/yewtube/commit/9a8893d29553d07bc75acabb2adbdab541a50c84))

* Add X command to copy stream link ([`ccdb148`](https://github.com/mps-youtube/yewtube/commit/ccdb148fd73f9f2dc5ad4cbc78c5f1535216d59c))

* Fix down_many syntax parsing by copying regex from parse_multi() (#1)

TODO: figure out if this can be simplified ([`c186d0e`](https://github.com/mps-youtube/yewtube/commit/c186d0e22ef4bcd0b6f3875212c7b7a4d9d79839))

* Show stream details under stream info section ([`99da435`](https://github.com/mps-youtube/yewtube/commit/99da4358ff92012239db6fdaa53f22d90da49b28))

* Show stream details in video information ([`8180ced`](https://github.com/mps-youtube/yewtube/commit/8180cedc717b9698a37b5f763183b23c6cfa2f26))

* Merge pull request #677 from paulfertser/comment-replies

misc: retrieve and show comment replies ([`3fa3fb2`](https://github.com/mps-youtube/yewtube/commit/3fa3fb285ed7ec2c65658ea20b7ec580c4e3ec0a))

* misc: retrieve and show comment replies

Signed-off-by: Paul Fertser &lt;fercerpav@gmail.com&gt; ([`6fb1265`](https://github.com/mps-youtube/yewtube/commit/6fb12657c9cf64e6dd87499565e922aac26fb889))

* Fix down_many syntax parsing by copying regex from parse_multi()

TODO: figure out if this can be simplified ([`1176566`](https://github.com/mps-youtube/yewtube/commit/11765660293f356878bc7fb8fbbc5f88582a4d20))

* Merge pull request #664 from ritiek/develop

Fixes #663 ([`a48d2fc`](https://github.com/mps-youtube/yewtube/commit/a48d2fc013383b6dc3421ca073628c7cd424a0e5))

* Fix playlist searching bug in rare cases ([`3399454`](https://github.com/mps-youtube/yewtube/commit/33994547275159b6ab59975e2ddaf94d72d85f1f))

* Remove debug code ([`a6f51d7`](https://github.com/mps-youtube/yewtube/commit/a6f51d7d5acd2ee2cc88e33942616ae3492cb30e))

* Stick to PEP-8 rules ([`3fdea83`](https://github.com/mps-youtube/yewtube/commit/3fdea8337a24ae9f2242bbe1c830d3600a3c1bc2))

* Fixes #663 ([`4ec2835`](https://github.com/mps-youtube/yewtube/commit/4ec28353aabdd6018c00e56cde9247ccf9b8db41))

* Skip softrepeat if len(songlist) &gt; 1 ([`b5d594b`](https://github.com/mps-youtube/yewtube/commit/b5d594b29af73226fd77672a1dd4a33b01e0425a))

* Preserve mpv options and cache when using repeat ([`0cab3a4`](https://github.com/mps-youtube/yewtube/commit/0cab3a4705a65ba1fd1b7126bb9e0fb04a548f8d))

* Merge pull request #656 from Vrihub/video_format

Add new configuration option: video_format ([`2746bf5`](https://github.com/mps-youtube/yewtube/commit/2746bf5f89ae31becab652ed141de2355d0a0910))

* Add new configuration option: video_format

Add the video_format configuration option, to let the user choose the
preferred video format for downloads, in a way similar to the current
audio_format option. See https://github.com/mps-youtube/mps-youtube/issues/529 ([`bbc9155`](https://github.com/mps-youtube/yewtube/commit/bbc915599a0081542b44bc3a34599512366c5658))

* Remove ^ from mplayer version regex

This was causing issues due to ansi escape codes at the start. ([`954824d`](https://github.com/mps-youtube/yewtube/commit/954824d3fb4b6f8ebbbd5fe6d33a1adbd4981596))

* Install listview/ ([`e10030b`](https://github.com/mps-youtube/yewtube/commit/e10030b336e15a774dc83c9f603a6bbfc41cf64d))

* Adds new text parsing algorithm ([`3e885b6`](https://github.com/mps-youtube/yewtube/commit/3e885b69aab114043fac27a5e8ec067bca729a12))

* Handles events where fetch_songs return no results ([`e07a117`](https://github.com/mps-youtube/yewtube/commit/e07a1176c23af23ed5bfc8e398e41bed2b2a39b4))

* Adds helptext and minor pylinting

Adds mkp to the search helptext keywords, adds --description help text.

Changed some _len(varname) &gt; 0:_ as this is the same as _if varname:_ ([`bc87af1`](https://github.com/mps-youtube/yewtube/commit/bc87af165c703f14bdd2989262040aa273117248))

* Implements playlist generation based on video descriptions

Extends mkp functionality by having it act on the --description parameter.

When the --description parameter is passed, the software looks through g.model for suitable datatypes. It will find the first applicable object based on numerical input from the user, download that videos description and parse it for artist - track combinations, and will store that in a local playlist using the existing generate_playlist functionality. ([`4915a07`](https://github.com/mps-youtube/yewtube/commit/4915a0703145ec23a4f2d916922e1303ff490744))

* Enable generate_playlist to use specified titles, instead of only random

Old generate_playlist function only used random playlist names.
Defaults to random if no title is specified. ([`5899ffd`](https://github.com/mps-youtube/yewtube/commit/5899ffdbbfa6f5bcfd5bdc9b3826f056140298cf))

* Adds song extraction function fetch_songs() 

fetch_songs uses a series of regex expressions to filter out
&#34;artist - title&#34; combinations from mixed text input. ([`b67f1c0`](https://github.com/mps-youtube/yewtube/commit/b67f1c0d0a4deeeda9fd4cbc00ada272283ff382))

* Adds help function to parse comma separated number ranges

1, 2, 3, 7-11 etc ([`eed6437`](https://github.com/mps-youtube/yewtube/commit/eed6437f59048db3040640ee9b32de6428387bc0))

* Moves ListView to its own module

ListView file was getting somewhat large, I wanted to split it up into separate files to make it easier to find the applicable datatype. ([`4a432f8`](https://github.com/mps-youtube/yewtube/commit/4a432f8a293f0277fdbada9a0be3231eea8db676))

* Merge pull request #648 from fernandolguevara/develop

FIX - AttributeError: &#39;int&#39; object has no attribute &#39;encode&#39; ([`0c6db81`](https://github.com/mps-youtube/yewtube/commit/0c6db8174e9b76d6f1db5d4f83e795222e95f0c1))

* Merge pull request #1 from fernandolguevara/fernandolguevara-attr-error

FIX - AttributeError: &#39;int&#39; object has no attribute &#39;encode&#39; ([`2478b30`](https://github.com/mps-youtube/yewtube/commit/2478b306210e204254eb14e110addad2af42fe50))

* FIX - AttributeError: &#39;int&#39; object has no attribute &#39;encode&#39;

Traceback (most recent call last):
  File &#34;mpsyt&#34;, line 2, in &lt;module&gt;
    import mps_youtube.main
  File &#34;C:\Users\XXXXXXXXXX\projects\mps-youtube\mps_youtube\__init__.py&#34;, line 8, in &lt;module&gt;
    init.init()
  File &#34;C:\Users\XXXXXXXXXX\projects\mps-youtube\mps_youtube\init.py&#34;, line 58, in init
    cache.load()
  File &#34;C:\Users\XXXXXXXXXX\projects\mps-youtube\mps_youtube\cache.py&#34;, line 41, in load
    streams.prune()
  File &#34;C:\Users\XXXXXXXXXX\projects\mps-youtube\mps_youtube\streams.py&#34;, line 35, in prune
    util.dbg(c.b + &#34;paf: %s, streams: %s%s&#34;, len(g.pafs), len(g.streams), c.w)
  File &#34;C:\Users\XXXXXXXXXX\projects\mps-youtube\mps_youtube\util.py&#34;, line 86, in dbg
    logging.debug(*(xenc(i) for i in args))
  File &#34;C:\Users\XXXXXXXXXX\projects\mps-youtube\mps_youtube\util.py&#34;, line 86, in &lt;genexpr&gt;
    logging.debug(*(xenc(i) for i in args))
  File &#34;C:\Users\XXXXXXXXXX\projects\mps-youtube\mps_youtube\util.py&#34;, line 105, in xenc
    return utf8_replace(stuff) if not_utf8_environment else stuff
  File &#34;C:\Users\XXXXXXXXXX\projects\mps-youtube\mps_youtube\util.py&#34;, line 99, in utf8_replace
    txt = txt.encode(sse, &#34;replace&#34;).decode(sse)
AttributeError: &#39;int&#39; object has no attribute &#39;encode&#39; ([`f217cbe`](https://github.com/mps-youtube/yewtube/commit/f217cbeab5d2ea74dd9a983d9a5e2ba723faba46))

* replace left out instances of genpl with mkp ([`efedc0d`](https://github.com/mps-youtube/yewtube/commit/efedc0dcdef074fc5779342becd3bad3632d72a6))

* changed genpl to mkp, modified _best_song_match to allow different weights, used it to return best match for mkp ([`4f7c156`](https://github.com/mps-youtube/yewtube/commit/4f7c1562a4d99cbb11cd41e1a3327426de23c788))

* Adhere to PEP 257 in docstrings ([`333c171`](https://github.com/mps-youtube/yewtube/commit/333c17191e8613aaa064d8daf398f7c00235ed69))

* Added genpl command to automatically generate playlist from video titles in a text file ([`ae29a0f`](https://github.com/mps-youtube/yewtube/commit/ae29a0ff3beecf38a416f9a9a683ce26869ae397))

* Merge pull request #638 from Razesdark/develop

Fixes bug with --category search ([`1a9cf1c`](https://github.com/mps-youtube/yewtube/commit/1a9cf1c55aaeeadf9eee565a6f194d8cb87d90d9))

* Fixes bug with --category search ([`e34d2f0`](https://github.com/mps-youtube/yewtube/commit/e34d2f010ec8c918a2d11671471c61e68ee7b66f))

* Merge pull request #635 from Razesdark/livestream_search_#634

Implements livestream search #634 ([`9e3006e`](https://github.com/mps-youtube/yewtube/commit/9e3006edf053c40e39260ef5894949ec71fd4e69))

* Updates Helptext for search arguments

Updates help text for all, including the two new search 
arguments. ([`1673602`](https://github.com/mps-youtube/yewtube/commit/1673602ea4514bff9863415da2a6a602c54a5569))

* Adds args to /search for filtering livestreams and categories

Adds -l/--live or -c/--category argument that can be used when searching to show livestreams and/or different categories.

The category scan can be used without using the --livestream scan ([`3ae33d9`](https://github.com/mps-youtube/yewtube/commit/3ae33d9b78e91cef867cf3f783b1bd4c7715e606))

* Adds &#34;live category&#34; command to software

Lets the user search for livestreams based on a categories. ([`2a9dd19`](https://github.com/mps-youtube/yewtube/commit/2a9dd19e8bfde929bd9473b1a248925f402200e6))

* Makes ListView._run parse ranges and lists, and return array ([`cec81e1`](https://github.com/mps-youtube/yewtube/commit/cec81e1fb5b766e33782e48841c60091a5878462))

* Merge pull request #633 from tochev/patch-1

Fix py3.4 dict creation compatibility ([`66914bf`](https://github.com/mps-youtube/yewtube/commit/66914bf5b266d95fd290c69df7150537cf0a67e9))

* Fix py3.4 dict creation compatibility ([`a3f4c9c`](https://github.com/mps-youtube/yewtube/commit/a3f4c9cd2ba07d69609fd0f7cf1b37eda9c32afe))

* Remove explicit inheritance from object

Unneeded in Python 3 ([`0933150`](https://github.com/mps-youtube/yewtube/commit/09331502a808560246d7e460b714952623ed41c8))

* Remove a &#34;del&#34; ([`1840cd9`](https://github.com/mps-youtube/yewtube/commit/1840cd9258655ef698f31e8dd6aba4bee7b27b80))

* make ListView a subclass of PaginatedContent ([`8779160`](https://github.com/mps-youtube/yewtube/commit/8779160ae185680bc80cc35e0a7b02d19559c86c))

* Adds two more lines in listview ([`160f8ae`](https://github.com/mps-youtube/yewtube/commit/160f8ae151f499c5d87ee6418b3fc37b04a2644f))

* Adds pagenumbers to list view ([`028e2ab`](https://github.com/mps-youtube/yewtube/commit/028e2abecafc04ba7cc4f2fdd5b5c9b5a4f64268))

* Fixes wrongly named variable in play ([`0894438`](https://github.com/mps-youtube/yewtube/commit/089443824c35e1cadda715d008237ff32f1bf920))

* Adds channel search ([`3964a4f`](https://github.com/mps-youtube/yewtube/commit/3964a4f182da49f88a518a0bfa646b23c5091ca7))

* Improves user search per #618 ([`8e3207e`](https://github.com/mps-youtube/yewtube/commit/8e3207e296796e5fcd40ff68407f883e7dbabbb7))

* Merge pull request #627 from Razesdark/id_column

Implements #623 - Adds Video ID to the list of available columns ([`15e16ea`](https://github.com/mps-youtube/yewtube/commit/15e16ea014abf8bd23dd4e5a9e2465520bbad287))

* Implements #623 ([`4bc8951`](https://github.com/mps-youtube/yewtube/commit/4bc89516ef0be459ad73720c1412786bfd6881bd))

* Merge pull request #626 from herbertjones/duration_help_typo_fix

typo in duration/after help text ([`7bd0cf6`](https://github.com/mps-youtube/yewtube/commit/7bd0cf689892145b617a05dbef22e949319eb04a))

* typo in duration/after help text ([`934a0af`](https://github.com/mps-youtube/yewtube/commit/934a0af2ef2a3ff3abff99a895c48bec74879917))

* Set current_page to 0 when displaying comments ([`8c38fc7`](https://github.com/mps-youtube/yewtube/commit/8c38fc74ee7d37adff2231bacc31a694eedee8a5))

* Deal with divide by zero error (#620) ([`bdea35d`](https://github.com/mps-youtube/yewtube/commit/bdea35d50f50fd0eaef036d9c7d762068df1f192))

* Merge pull request #619 from jwilk/re.sub

Fix misuse of flags in re.sub() call ([`136e00d`](https://github.com/mps-youtube/yewtube/commit/136e00d37a80390ab65a39b7bcf7d32f37574336))

* Fix misuse of flags in re.sub() call

The 4th argument of re.sub() is maximum number of substitutions,
not flags. ([`c883201`](https://github.com/mps-youtube/yewtube/commit/c8832018e943753caca879a82a8620f76e59698c))

* Fix bug in dbg() ([`48787b1`](https://github.com/mps-youtube/yewtube/commit/48787b189d83299a7489b4e19119974e0dac4b24))

* Update docker instructions to not use --privileged

Closes #606 ([`523775d`](https://github.com/mps-youtube/yewtube/commit/523775d269ddbb45a5fad62f8ed33181e1824771))

* Merge pull request #605 from orschiro/patch-1

Fixed wrong dbus python package ([`8d815b4`](https://github.com/mps-youtube/yewtube/commit/8d815b4e2840fde58b930c28537a8087ea2620af))

* Fixed wrong dbus python package ([`369cb83`](https://github.com/mps-youtube/yewtube/commit/369cb832debf54aa6d9905fa3a274ae52ef8ebae))

* Correct package name in README ([`d4ea9cc`](https://github.com/mps-youtube/yewtube/commit/d4ea9ccb9e26e6664528a192004c48e99e99e0e9))

* Merge remote-tracking branch &#39;ardrabczyk/title-mod-merge&#39; into develop ([`f096f91`](https://github.com/mps-youtube/yewtube/commit/f096f91f0546e93fcb5f5a9444f7fd60c2747f23))

* Add set_title config option ([`a63c376`](https://github.com/mps-youtube/yewtube/commit/a63c37653a2c262b0b423e1ec8b9f8cf2df49008))

* Make autoplay default to off ([`f682cb7`](https://github.com/mps-youtube/yewtube/commit/f682cb779dcd669f90324aa277d31005262239c5))

* Merge pull request #594 from nikhilweee/develop

Autoplay ([`a129742`](https://github.com/mps-youtube/yewtube/commit/a12974281b054033eab809ec847b6a2dd6d9c485))

* added autoplay feature ([`2efadd8`](https://github.com/mps-youtube/yewtube/commit/2efadd8b6377a70770b4612a3e4bc1980f101b0a))

* Fix syntax error ([`0574c72`](https://github.com/mps-youtube/yewtube/commit/0574c72d6f43dc8e6b86fa1c70cbe4ada1f89a10))

* Merge pull request #585 from glensc/url-update

update url ([`40ee807`](https://github.com/mps-youtube/yewtube/commit/40ee807fb3f818929f2e6ede32a65f0d1c75a32c))

* update url

http://github.com/np1/mps-youtube redirects to https://github.com/mps-youtube/mps-youtube ([`e773f51`](https://github.com/mps-youtube/yewtube/commit/e773f51b148efa575501dd3273fbd21952600142))

* convert UTC time returned from YouTube API to local time ([`79659b0`](https://github.com/mps-youtube/yewtube/commit/79659b0b2edad289aaaa9449bc1b24f8fef4f6db))

* add &#34;time&#34; column which shows uploaded time in UTC ([`504534a`](https://github.com/mps-youtube/yewtube/commit/504534ac9f4ef69dc503974f3541268601351f35))

* Updated the docker container in the README ([`62d9cf7`](https://github.com/mps-youtube/yewtube/commit/62d9cf784908d1a906b1cec8fb88c685f82673c5))

* Make sure variable is defined before try/finally ([`9e0f443`](https://github.com/mps-youtube/yewtube/commit/9e0f4431bad50d5e0eeee934fcff4dbfd0893b41))

* player.py: use TLS when retrieving art ([`38ed321`](https://github.com/mps-youtube/yewtube/commit/38ed321d3caf0a0b0d99c0c3cdaafac3b80ed576))

* Remove unused Playlist.creation ([`bea811f`](https://github.com/mps-youtube/yewtube/commit/bea811fda05b10041a389eb2c5984f8d6ad91303))

* Use .split() instead of .split(&#39; &#39;) ([`6ed1042`](https://github.com/mps-youtube/yewtube/commit/6ed1042875470a430397fec45a3fdb7b20153427))

* bit of clean up ([`9204f12`](https://github.com/mps-youtube/yewtube/commit/9204f126ce88d106ac1913328e89c1bd5061352f))

* Improve search parameter safety ([`0f45469`](https://github.com/mps-youtube/yewtube/commit/0f4546950e13ad082bc136248756423dbb7e83ab))

* switch to argsparse for new syntax ([`fa488b6`](https://github.com/mps-youtube/yewtube/commit/fa488b6438133647e0af277ed23dfe50ca8f3325))

* Merge branch &#39;search_after_date&#39; into develop

    # Conflicts:
    #   mps_youtube/commands/search.py
    #   mps_youtube/helptext.py ([`c38fa03`](https://github.com/mps-youtube/yewtube/commit/c38fa0376453739105e72e73fad3df039f77dd09))

* Merge pull request #1 from jas32096/search_duration

Search duration ([`070a86d`](https://github.com/mps-youtube/yewtube/commit/070a86dab105b1b7a067b4ba1adf12018138d61a))

* helptext tweak ([`656b3bd`](https://github.com/mps-youtube/yewtube/commit/656b3bd32e0898e69f0d650d39fb01c5ac2f35f8))

* Allow user to limit their searches to any, long, medium, and short duration buckets ([`c14c3ea`](https://github.com/mps-youtube/yewtube/commit/c14c3ead6fd604d873a732654a013343e69faabb))

* Mention dbus and gobject dependencies ([`2ee7604`](https://github.com/mps-youtube/yewtube/commit/2ee76048855ed5e09533403de21afb39e4f16bac))

* Fix error on missing gi.repository

Should be optional dependency ([`942cfed`](https://github.com/mps-youtube/yewtube/commit/942cfed76baa484a08ff58549f3d1032db37d9cb))

* Update README to recommend mpv ([`48d6b2b`](https://github.com/mps-youtube/yewtube/commit/48d6b2b8b5b57972fd2ef04983c62f074ff74210))

* Merge pull request #524 from sup/develop

Add mpv as a recommended player in mac installation section ([`603f6bc`](https://github.com/mps-youtube/yewtube/commit/603f6bc8bdb7bccdb0635a9556be2dbd52309bb3))

* Update mac installation instructions with mpv ([`1bef6c1`](https://github.com/mps-youtube/yewtube/commit/1bef6c133288b8115ff2b97517757d29f4b97935))

* Merge remote-tracking branch &#39;Ofloo/develop&#39; into develop ([`d525bf7`](https://github.com/mps-youtube/yewtube/commit/d525bf7faeb76fa373b5f0225f3e2d8537133cdb))

* Fixed zero devider

dvpl PLTmR6HsT7005r9J50_HCOGkyGc8dDYu7J ([`491c257`](https://github.com/mps-youtube/yewtube/commit/491c2579a1f80ddeac0141257c52c248aa53f145))

* Merge pull request #517 from Gongreg/develop

Added command --no-textart to disable textart, so users with screen reader wouldn&#39;t get confused by it ([`ab87e07`](https://github.com/mps-youtube/yewtube/commit/ab87e07dcfc4447b6d844973b704cb14467af119))

* Added command to disable text-art, so users with screen reader wouldn&#39;t get confused by it ([`79f9b87`](https://github.com/mps-youtube/yewtube/commit/79f9b876795b180c81c632373e1a82ce1077edae))

* Merge pull request #519 from pritambaral/patch-1

Handle mpv sending bad `time-pos` data ([`2e0a353`](https://github.com/mps-youtube/yewtube/commit/2e0a3535ebb699ea6fc07aa6146353209e93fb24))

* Handle mpv sending bad time-pos data

mpv sometimes sends `{&#34;event&#34;:&#34;property-change&#34;,&#34;id&#34;:1,&#34;name&#34;:&#34;time-pos&#34;,&#34;data&#34;:null}` on the socket; for example when the user has configured mpv (say, via `mpv.conf`) to loop over, then mpv sends this malformed event upon a new iteration of playback ([`f1f38a4`](https://github.com/mps-youtube/yewtube/commit/f1f38a458ca1041ba7fb68e3812a2291a4cdf6c7))

* Merge remote-tracking branch &#39;srvanrell/develop&#39; ([`8508c46`](https://github.com/mps-youtube/yewtube/commit/8508c46dae26ee04ea0f7ddcbb1bc0feb69add2a))

* Add help of history recent ([`e5627d8`](https://github.com/mps-youtube/yewtube/commit/e5627d833d326cee437db6cce8f812a7d6a70cfa))

* Add recent to history command ([`a84c96a`](https://github.com/mps-youtube/yewtube/commit/a84c96afab1f96df2e38a85e9244dd2908b00e38))

* Make regex handle liked videos playlists ([`5aba18a`](https://github.com/mps-youtube/yewtube/commit/5aba18ae7c7fd0cc46ed853f180f504b48fec2df))

* Version 0.2.7.1 ([`a9541cb`](https://github.com/mps-youtube/yewtube/commit/a9541cbff9b949bd273d3e8e54a6e53715589819))

* Install LICENSE, README.md, and CHANGELOG as package_data ([`93451ce`](https://github.com/mps-youtube/yewtube/commit/93451ce0e6214ce296317d7027c479e7d8239c81))

* Hopefully fix pickle error ([`401539e`](https://github.com/mps-youtube/yewtube/commit/401539e3e62e761a8b237fda76d008f3c430745a))

## v0.2.7 (2016-06-27)

### Unknown

* Version 0.2.7 ([`7639d35`](https://github.com/mps-youtube/yewtube/commit/7639d3525a0412887d05f77a2ab6d59848997825))

* Merge pull request #481 from PI-Victor/add_youtube_dl_to_dockerfile

add youtube_dl as a dependency to the Dockerfile ([`4f80b67`](https://github.com/mps-youtube/yewtube/commit/4f80b678d0d17bd18a123c388363c3ff74fd31c4))

* add youtube_dl as a dependency to the Dockerfile

*without this it will run into
https://github.com/mps-youtube/mps-youtube/issues/475 whenever trying to run mps
inside the docker container. ([`37f24ea`](https://github.com/mps-youtube/yewtube/commit/37f24ea95dd9672cdfcef9fe1ff3dc61680e569c))

* Correct PL regex ([`e6cd6dc`](https://github.com/mps-youtube/yewtube/commit/e6cd6dc2753bd89c95ae2698726d5f13eb1181e1))

* Pass --play-and-exit to vlc if used

Vlc is not supported, but this may help for those using it nevertheless. ([`e73059e`](https://github.com/mps-youtube/yewtube/commit/e73059ec3e3e45213aa562718f37adf4b22a977f))

* Parse arguments before doing anything else ([`79b09c1`](https://github.com/mps-youtube/yewtube/commit/79b09c19ec85e57a87c35f01f508b1ac8f74b44f))

* Pass --no-ytdl to mpv ([`9152509`](https://github.com/mps-youtube/yewtube/commit/9152509e820c2d822f5de643b264d73e07b2b7a3))

* Do not create input_file when player is neither mpv nor mplayer ([`2e70f85`](https://github.com/mps-youtube/yewtube/commit/2e70f859d9dcdbb51c40e94f67fe4621efd26272))

* Add g.mpv_options global ([`94c6b43`](https://github.com/mps-youtube/yewtube/commit/94c6b431da9c5e4cc093571cff025c888035f3e2))

* Added repetition x times feature ([`9611b41`](https://github.com/mps-youtube/yewtube/commit/9611b41458465d1dd9b33ddb1cc4f984a177d850))

* Update documentation ([`f61c0d0`](https://github.com/mps-youtube/yewtube/commit/f61c0d0a51cfbaa3eeeb998b32c14a61959a2b21))

* Make user_more work after url command ([`e3b1c9c`](https://github.com/mps-youtube/yewtube/commit/e3b1c9c665aa691dda482457ec146278aaf92176))

* Call _generate_real_playerargs() in _playsong() not _launch_player() ([`62df61b`](https://github.com/mps-youtube/yewtube/commit/62df61b37c75d5db9d7788ed6866e5c794b97d51))

* Remove documentation for no longer existing colours option ([`9ed3ca9`](https://github.com/mps-youtube/yewtube/commit/9ed3ca93ae9bf9034b24900ba19a18bd0dffc4b6))

* Make setup.py install commands submodule

Fixes #477 ([`ea9f338`](https://github.com/mps-youtube/yewtube/commit/ea9f338686c1f47cadc87f5ddd11b7cb563d38fd))

* Add uncommited documents file ([`3d8d086`](https://github.com/mps-youtube/yewtube/commit/3d8d086daec5374f107ec1b0034062e6eca17e23))

* Fix typo ([`512ab28`](https://github.com/mps-youtube/yewtube/commit/512ab28966dabb220b8fbe683ebe777f77abbf95))

* Correct return values in docstrings ([`01a014e`](https://github.com/mps-youtube/yewtube/commit/01a014ebd7e8291593caa8d542ab39340d8429ca))

* Correct rst syntax ([`bd6805b`](https://github.com/mps-youtube/yewtube/commit/bd6805b422681ad6077aff6f17de693c23d68556))

* Improve docstrings ([`e9d1ffa`](https://github.com/mps-youtube/yewtube/commit/e9d1ffa7c4095e5bf0fcb9b2c6f386ac27167624))

* Document paginatesongs() ([`8bbc859`](https://github.com/mps-youtube/yewtube/commit/8bbc8598c00345f0bcba163a6042e7781b320f3b))

* Update F() docstring ([`d54ac36`](https://github.com/mps-youtube/yewtube/commit/d54ac36570b6feae446ccef88085ad2127244389))

* Add sphinx docs, generated with sphinx-apidoc ([`c952126`](https://github.com/mps-youtube/yewtube/commit/c952126ae63cb9bc18aa17bdcb44173e058fc570))

* Remove unneeded Windows specific color code ([`256b347`](https://github.com/mps-youtube/yewtube/commit/256b3470eec5d0ab0cb6a5c445914b87a7efb9ad))

* Use ininstance() instead of type()..is ([`5af7e12`](https://github.com/mps-youtube/yewtube/commit/5af7e1240d265560e366e96b215a2b690bcddb1c))

* Import util rather than functions therof; same with content ([`299d540`](https://github.com/mps-youtube/yewtube/commit/299d5408f4bb6129f706c249ad38629cbcd0c221))

* Import module instead of function ([`a07ef5f`](https://github.com/mps-youtube/yewtube/commit/a07ef5fa1d5d8111fdf79291c947b8c4325c450b))

* Fix error in older python version ([`a7c0bcd`](https://github.com/mps-youtube/yewtube/commit/a7c0bcd34c08b8ed4cbe139ed7958721489aabf0))

* Use &#34;import config&#34; instead of &#34;from config import Config&#34; ([`c49de53`](https://github.com/mps-youtube/yewtube/commit/c49de53a42ec9e65aab2c177e06b3ef48857b6dd))

* Move load_player_info() and is_known_player() to util.py ([`a759d0b`](https://github.com/mps-youtube/yewtube/commit/a759d0bea003a604f3010cfe31517cc5f9f2bdf9))

* Make known_player_set() and load_player_info() take player as argument

Also rename known_player_set() to is_known_player() ([`6ab8ec3`](https://github.com/mps-youtube/yewtube/commit/6ab8ec3b2c663686737a82245a6f5884c53c9ead))

* Corrections ([`d779785`](https://github.com/mps-youtube/yewtube/commit/d7797858032c7308fcc7c72c5699b8e43fd513e0))

* Reduce use of function imports (rather than module imports) ([`fc5a543`](https://github.com/mps-youtube/yewtube/commit/fc5a543269903bc96ac58233832d25e118eef91f))

* Mention youtube_dl in README ([`f2cbdfa`](https://github.com/mps-youtube/yewtube/commit/f2cbdfa4082d6a6ce69758433540b078c6f30f42))

* Remove unused import ([`39980b6`](https://github.com/mps-youtube/yewtube/commit/39980b613fac943f2dee93ec3728ba4a3aff90e5))

* Simplify get_near_name() ([`027dec6`](https://github.com/mps-youtube/yewtube/commit/027dec6606452108ab208057d112ebb0aaf16a20))

* Remove landscape compatability code, since landscape now has py3 ([`5f79f6f`](https://github.com/mps-youtube/yewtube/commit/5f79f6f4cf3736843a66d88e73fd5048842d37f0))

* Remove unused import ([`cfac154`](https://github.com/mps-youtube/yewtube/commit/cfac154051b6320b9b7a0db4f799618ed4e98e5b))

* Add comment ([`e357a5d`](https://github.com/mps-youtube/yewtube/commit/e357a5d62f5777f82d4836c9de08bf73e012f101))

* Avoid shadowing name ([`f543fd1`](https://github.com/mps-youtube/yewtube/commit/f543fd173c683ce054f0985012ca6d76aac7c79c))

* Rename word, pl, and rs to WORD, PL, and RS ([`cdf537d`](https://github.com/mps-youtube/yewtube/commit/cdf537d32e151745f75f2d83d2ce28a69abb4d0a))

* Add missing line ([`6feadf3`](https://github.com/mps-youtube/yewtube/commit/6feadf3f2bb983b437090f06a9ba87c27810f3fe))

* Remove unused import ([`d6b7a13`](https://github.com/mps-youtube/yewtube/commit/d6b7a1385b7a58c13f01f30c13657148ed914b02))

* Remove command definitions from main, and break them into several files ([`2117ded`](https://github.com/mps-youtube/yewtube/commit/2117ded3a27bd2e0345266f1f22fe85771cbe2cf))

* Move commands.py to comands/__init__.py ([`fd85ce4`](https://github.com/mps-youtube/yewtube/commit/fd85ce45d716e6485ffa9470a2ecb3cd5e6f40ea))

* Move IterSlicer to util.py ([`fcb7173`](https://github.com/mps-youtube/yewtube/commit/fcb71731ab83832bb59e4a9b86f45a392289812e))

* Add missing import ([`0540f51`](https://github.com/mps-youtube/yewtube/commit/0540f51bb67b6b2f9552bd0eef688a7afefa14dc))

* Move load/save playlist to new file ([`8b95f1b`](https://github.com/mps-youtube/yewtube/commit/8b95f1ba49f2b14a222c4ead1c80b74317f9ba47))

* Move playlists_display() to content.py ([`5049916`](https://github.com/mps-youtube/yewtube/commit/5049916b930fbe56b45caa025be542a3674998de))

* Move parse_multi() to util ([`32d562c`](https://github.com/mps-youtube/yewtube/commit/32d562c27528ca1efe2810ea9814dee6c38ac2d2))

* Fix import ([`c5c6db1`](https://github.com/mps-youtube/yewtube/commit/c5c6db12d1f749317044d17f9624f4400ec4c75d))

* Add missing import ([`d28375c`](https://github.com/mps-youtube/yewtube/commit/d28375cfce73e2546263bc211a5bf71d46f515fb))

* Add missing import ([`381c5fc`](https://github.com/mps-youtube/yewtube/commit/381c5fcdec0aaade91ebc92e554232fb20d5344d))

* Move get_user_columns() and logo() to content.py ([`aa98f5d`](https://github.com/mps-youtube/yewtube/commit/aa98f5d69634fad5e40485552857c3fdff2ce561))

* Move generate_{songlist,playlist}_display() to content.py ([`94fa235`](https://github.com/mps-youtube/yewtube/commit/94fa235e01feb99891c1d96c66a238740726ea39))

* Actually, that import shouldn&#39;t have been removed ([`6d9c78c`](https://github.com/mps-youtube/yewtube/commit/6d9c78c74dfb4961068bae66a53a40a6e548d6cc))

* Correct some imports ([`1f92224`](https://github.com/mps-youtube/yewtube/commit/1f92224683ba73a41e5108a8396e6631973004ad))

* Move play_range() to player.py ([`19fb985`](https://github.com/mps-youtube/yewtube/commit/19fb98544d2c0d2a626645bd9d9a8f3be62fb74b))

* Call generate_songlist_display() in play(), not play_range() ([`39499da`](https://github.com/mps-youtube/yewtube/commit/39499da6835d16ee90fb4c412d4e95af1f8c99ba))

* Move preload to streams ([`f230bba`](https://github.com/mps-youtube/yewtube/commit/f230bba4d88de23172dc064ed2b03e2cf190403d))

* Move playsong to player.py, and history commands to history.py ([`3cd3d02`](https://github.com/mps-youtube/yewtube/commit/3cd3d02b7db9d620b56b2cde1692e87f8ee0e828))

* Correctly handle player switching ([`16b6da4`](https://github.com/mps-youtube/yewtube/commit/16b6da4cca9379c486b4436046a261c42bc6bc70))

* Fix for argument rename in mpv 0.17.0 ([`7c2470f`](https://github.com/mps-youtube/yewtube/commit/7c2470f1eea4089014f38f451277623999c01c14))

* Speed up shutdown by avoiding redirects in checkupdate ([`f87fa3a`](https://github.com/mps-youtube/yewtube/commit/f87fa3a12dd894636e33953efdb503ae3288e412))

* Fix pyperclip support ([`dbd0a98`](https://github.com/mps-youtube/yewtube/commit/dbd0a983f461dc9e70e96f2d0df1e0d00fe75653))

* Improve message on failure of copy to clipboard ([`5c877ff`](https://github.com/mps-youtube/yewtube/commit/5c877ff54f6436a0bfc5b8d2a5af21da74e9f028))

* Make IterSlicer.__len__ not need to load entire list ([`71233f1`](https://github.com/mps-youtube/yewtube/commit/71233f18571358409ba0e9611107575d0ef83acb))

* Make &#34;reverse all&#34; work with IterSlicer lists ([`f439c1f`](https://github.com/mps-youtube/yewtube/commit/f439c1f6c80c3b98549f92235e0f7b2b0132f59e))

* Merge remote-tracking branch &#39;kraetzin/develop&#39; into develop ([`3e19dfa`](https://github.com/mps-youtube/yewtube/commit/3e19dfada9759845bccdfaf8063705f431cfcee9))

* By default, display latest played song first in history ([`de06e91`](https://github.com/mps-youtube/yewtube/commit/de06e91f14c5f8cd469cacacc108e31416d2662a))

* Removed redundant line. ([`ffb79ca`](https://github.com/mps-youtube/yewtube/commit/ffb79ca6401d8d4b0ee80e27f0575f12952a8fa5))

* Prevented crash when &#39;reverse all&#39; called on playlist search. Handled exception ([`c98aee0`](https://github.com/mps-youtube/yewtube/commit/c98aee04534ea037b7f28562b820ba491ede4ea4))

* Additions to help and prevented crash ([`b176890`](https://github.com/mps-youtube/yewtube/commit/b17689015f2cbc5f8712d862483d95f3b4974f56))

* Changed upper limit of func to None ([`e8081cb`](https://github.com/mps-youtube/yewtube/commit/e8081cbf8ff985aa95463512ba25b05bf048d16a))

* Added function to reverse whole loaded playlist ([`8091c0f`](https://github.com/mps-youtube/yewtube/commit/8091c0fe12968af510c4fa419ba0648d195a6f92))

* Added reverse range function ([`b9775e3`](https://github.com/mps-youtube/yewtube/commit/b9775e304f4db7645402ada1ec3079dd121c3df7))

* Added reverse command for song list ([`96b45e8`](https://github.com/mps-youtube/yewtube/commit/96b45e88a6184acb1d52767b06027f00171dd35f))

* Merge pull request #472 from kraetzin/develop

Add a history of played songs ([`e0b17a1`](https://github.com/mps-youtube/yewtube/commit/e0b17a13fe1a6fee8eecc181db00670e44d64e9d))

* Removed redundant line ([`f7b5966`](https://github.com/mps-youtube/yewtube/commit/f7b59665415c00c7273c763f8da253726d12261a))

* Changed when a song is added to history ([`3851b48`](https://github.com/mps-youtube/yewtube/commit/3851b483a5d7d51573051cad382638c64ae250f3))

* Removed redundant line ([`ab0483a`](https://github.com/mps-youtube/yewtube/commit/ab0483a7ea691f134d1c6d875cc614eddd3075b3))

* Added help text ([`15f39ed`](https://github.com/mps-youtube/yewtube/commit/15f39ed82e798e513d0823e8abaed52ca9d3ef8e))

* Revert &#34;Added help text&#34;

This reverts commit 96b43bc0d9ea84b94b5e601390261b4f96a7e018. ([`85bf44c`](https://github.com/mps-youtube/yewtube/commit/85bf44cd76965444f3bc12e8ef3483ceacca2c76))

* Added help text ([`96b43bc`](https://github.com/mps-youtube/yewtube/commit/96b43bc0d9ea84b94b5e601390261b4f96a7e018))

* Removing changes to gitignore ([`a4c5371`](https://github.com/mps-youtube/yewtube/commit/a4c53714593c7aeb4b822880d906b621ac144e44))

* Add function to clear history ([`4f27257`](https://github.com/mps-youtube/yewtube/commit/4f272575fd333b07e8a5a64aefa71d4eac3d2c51))

* Add function to view history ([`21bd6b6`](https://github.com/mps-youtube/yewtube/commit/21bd6b6b81463e5a9f7f067612ee7af36f10ed10))

* Actually add the history_add function ([`f00386c`](https://github.com/mps-youtube/yewtube/commit/f00386c78b290be3c5c73ec773950a106c6aafcc))

* Remove swp files ([`cd32730`](https://github.com/mps-youtube/yewtube/commit/cd32730fb4c84a5237af32c7edd5bbe62c5d1034))

* Remove swp files ([`e703c3e`](https://github.com/mps-youtube/yewtube/commit/e703c3e97352954c20249d674b2adb76dbce0506))

* Added function to add song to history. Called each time a song is successfully loaded ([`9013cce`](https://github.com/mps-youtube/yewtube/commit/9013cce98726f336e1da8cffb98a029105d46b41))

* Actually open history file in main ([`38b7c49`](https://github.com/mps-youtube/yewtube/commit/38b7c490fc5f5a28cc40366cc74196d22feb293f))

* Actually open history file in main ([`04a8e37`](https://github.com/mps-youtube/yewtube/commit/04a8e37eef8d2a99a651f060e1a2ef3d767bbd47))

* Added opening of history file ([`33f36e0`](https://github.com/mps-youtube/yewtube/commit/33f36e0f7775803bd42b02a0f5fc1f6aaa0daa39))

* Created globals for history dict and history file ([`c7c827d`](https://github.com/mps-youtube/yewtube/commit/c7c827db86b77704d9466b135f5acb7b9cd48878))

* Merge pull request #467 from nishanthkarthik/develop

Add settings for default audio format ([`ff72165`](https://github.com/mps-youtube/yewtube/commit/ff72165e9d1c0ab3322f1057b33cfd91069417aa))

* Add settings for default audio format ([`c6cf3c0`](https://github.com/mps-youtube/yewtube/commit/c6cf3c0f5d32c1fcb175d54423ba95a6ad33f75c))

* Remove unused imports ([`3d86b5b`](https://github.com/mps-youtube/yewtube/commit/3d86b5b45d16187f7a1c22d0a7780c18fd66ede2))

* Remove use of unimported class ([`4ea19d0`](https://github.com/mps-youtube/yewtube/commit/4ea19d01c2d532706fd46bf51565dbab4ed5a468))

* Fix entry point ([`d100df9`](https://github.com/mps-youtube/yewtube/commit/d100df964494b67114a298854889f8747c63199c))

* Move init to new file, init.py ([`6b002d5`](https://github.com/mps-youtube/yewtube/commit/6b002d567a64e1559fd6adcf2e168c3648e32b20))

* Call generate_real_playerargs from launch_player() ([`3b3604d`](https://github.com/mps-youtube/yewtube/commit/3b3604d47e6656e2137ca441ad631fa056fe7ba9))

* Move generate_real_playerargs to player.py ([`02d1a5c`](https://github.com/mps-youtube/yewtube/commit/02d1a5c21ccf120bc72797bd2eebf730b36699f8))

* Move songdata code out of generate_real_playerargs ([`ca0594e`](https://github.com/mps-youtube/yewtube/commit/ca0594e21e428c285bda076ed278dceb5232e599))

* Move song selection out of generate_real_playerargs ([`b915e1e`](https://github.com/mps-youtube/yewtube/commit/b915e1ec36987bad17ec0727bb4be13f9e33d999))

* Make --version show pafy backend info (on newest pafy) ([`024d518`](https://github.com/mps-youtube/yewtube/commit/024d5187a42f811ba6765bd5c9349fec200492a0))

* Correct import ([`ddb793b`](https://github.com/mps-youtube/yewtube/commit/ddb793b13f146fe06c88f55893ebdda561db8b4b))

* Fix bug in playlist info ([`f95b552`](https://github.com/mps-youtube/yewtube/commit/f95b5523cf596f8a12020443166ca4270a84be16))

* Move getxy() to util to fix circular import ([`3db14b4`](https://github.com/mps-youtube/yewtube/commit/3db14b4c3ddec574de6b71d439ca532fe9fa1aca))

* Fix album search ([`0f56b70`](https://github.com/mps-youtube/yewtube/commit/0f56b700d835145dd6e154d13060bd467fb7b48e))

* Create new content api, and use it for comment pagination ([`1f77423`](https://github.com/mps-youtube/yewtube/commit/1f77423f7bd2db6ede91d2b3cb1751d81b9cb559))

* Slight change to paginatesongs ([`1c52473`](https://github.com/mps-youtube/yewtube/commit/1c52473a31cf28c8568311a424ff1524ea7f4169))

* Remove unneeded code ([`9ffa52e`](https://github.com/mps-youtube/yewtube/commit/9ffa52e49b75f633747267cf6222cd100c33a071))

* Remove a little duplication ([`f2dc5da`](https://github.com/mps-youtube/yewtube/commit/f2dc5dafcdf8c317730bc69fff031a82a6143f05))

* Small simplification ([`4964999`](https://github.com/mps-youtube/yewtube/commit/4964999f9df89ff37fceec06aae0df9744f91ec7))

* In debug mode, print tracebacks without exiting ([`b7e3ba1`](https://github.com/mps-youtube/yewtube/commit/b7e3ba1105215267ad166001d2f6e4476abc2d4b))

* Fix preloading bug (#416) ([`d0dd276`](https://github.com/mps-youtube/yewtube/commit/d0dd2767dc76a43dfd4fd76605519b069d231ea8))

* Add $ to end of play command regex

Needed to prevent greedy matching of middle group taking the - from the
last group ([`d9fcda2`](https://github.com/mps-youtube/yewtube/commit/d9fcda2814170f1fcb2c819a88770c49919c8f8b))

* Regex simplification ([`639c819`](https://github.com/mps-youtube/yewtube/commit/639c819cf288bc2e097aec1cb7994e69ac1c406c))

* Fix set regex ([`ca7e37d`](https://github.com/mps-youtube/yewtube/commit/ca7e37d7e37b1b2637edeb0ea0453b2d17978b08))

* Move player code to new file ([`6c77c57`](https://github.com/mps-youtube/yewtube/commit/6c77c57738906d0c30d2dd1298042868962f4da1))

* Don&#39;t use fullmatch, since that was added in python 3.4 ([`904408b`](https://github.com/mps-youtube/yewtube/commit/904408b6504771ae594cef55c086fef1a7b63e6e))

* Put LICENSE README and CHANGELOG in /usr/share/mps-youtube

It was placing them in /usr.
Closes #412. ([`a2a11ae`](https://github.com/mps-youtube/yewtube/commit/a2a11ae88b66612975284fe35192f7ee35f8ecd5))

* Do not use exename in mpv version regex

Fixes #397. ([`4ba1d41`](https://github.com/mps-youtube/yewtube/commit/4ba1d41e12624c4df1d5b57a0fba2e9cf75bab78))

* Implement Playlist.__setitem__, fixing sw command

As pointed out by @gitsper. Closes #407. ([`9d7ab49`](https://github.com/mps-youtube/yewtube/commit/9d7ab49478779b5e52ff680187cbc794d8685cd5))

* Merge pull request #402 from maricn/download_best_audio_by_url

Added option &#39;daurl &lt;url&gt;&#39; for downloading best audio by YouTube url. ([`23cc953`](https://github.com/mps-youtube/yewtube/commit/23cc953a43d85fee96d01d19087d43025e6ea99a))

* Added option &#39;daurl &lt;url&gt;&#39; for downloading best audio by YouTube url. ([`70b36c5`](https://github.com/mps-youtube/yewtube/commit/70b36c578db28c14e9b06f590074df717bddbcde))

* Do not supress mpv output when in debug mode ([`ca4fb4d`](https://github.com/mps-youtube/yewtube/commit/ca4fb4d5335abd0cbdeb66c509ce30d36ffff83b))

* Some refeactoring of generate_real_playerargs() ([`714d925`](https://github.com/mps-youtube/yewtube/commit/714d9254fa3ce4ee90033a17ef88ac0cef31b7ea))

* Minor syntax simplification ([`2fdb418`](https://github.com/mps-youtube/yewtube/commit/2fdb418f0eaa86ba386c4f0913fff3aa4bcce9d4))

* Use list comprehension instead of for loop ([`e4970cd`](https://github.com/mps-youtube/yewtube/commit/e4970cdd5b0af144e4a501e9933f45ae04fbc95b))

* Remove compatability code for old pafy ([`58aa398`](https://github.com/mps-youtube/yewtube/commit/58aa39845c63fc8f41784e0433a4546e12fee5a2))

* Make usersearch_id() syntax saner ([`01340f4`](https://github.com/mps-youtube/yewtube/commit/01340f42939d839360a6d501af61048f8461a9d9))

* Fix user_more() ([`9147ed6`](https://github.com/mps-youtube/yewtube/commit/9147ed68a7361b0556949c1788c40892118129ef))

* Fix result_count for userpl ([`441ef5d`](https://github.com/mps-youtube/yewtube/commit/441ef5d7a50f0a813c8903cb74b62a057fa61b80))

* Remove get_track_id_from_json() function ([`7064944`](https://github.com/mps-youtube/yewtube/commit/70649443976d8fc910615f71f600caf526745f37))

* Remove unneeded code ([`ac0a657`](https://github.com/mps-youtube/yewtube/commit/ac0a657c8fc6260ec16b6784a55715d643768a6f))

* Remove g.more_pages ([`0623839`](https://github.com/mps-youtube/yewtube/commit/06238391bc6168521f4358c3a1d415b7bba11664))

* Remove unneeded max() ([`ec81757`](https://github.com/mps-youtube/yewtube/commit/ec81757d5a54457b39f0d54d6be7d67f1ab7dfb7))

* Only limit to 500 for searches, not things like local playlists ([`86ef167`](https://github.com/mps-youtube/yewtube/commit/86ef1673523f98de966c06b4a50e3f68553147e3))

* Include LICENSE README and CHANGELOG in source distribution ([`ca69fb6`](https://github.com/mps-youtube/yewtube/commit/ca69fb61aca8346140c0392c65ffdd10dfe65437))

## v0.2.6 (2016-01-01)

### Unknown

* Version 0.2.6 ([`6f1bc54`](https://github.com/mps-youtube/yewtube/commit/6f1bc54d56c3c3a7d5509268d1442f979356def3))

* Fix filename handling in muxing code ([`f7ee349`](https://github.com/mps-youtube/yewtube/commit/f7ee3490cb9481326cca8d4a9b3870df1005ee6b))

* Remove no longer needed query and splash parameters ([`82e6fba`](https://github.com/mps-youtube/yewtube/commit/82e6fba3421994f889226492f40b0501b99ae6aa))

* Correct page_msg output ([`35bd1be`](https://github.com/mps-youtube/yewtube/commit/35bd1bebe395ca63221893326d1e526653270bac))

* Remove unneeded int() call ([`376674c`](https://github.com/mps-youtube/yewtube/commit/376674c9a011af7dd9b9cd5523dfae6868e09dfc))

* More preload thread starting code to function ([`314e434`](https://github.com/mps-youtube/yewtube/commit/314e4343e9635b04d1af700bcdf6fd6bffca4270))

* Do not explicitly pass default parameters to paginatesongs ([`6eeacad`](https://github.com/mps-youtube/yewtube/commit/6eeacad1232424d98ac8f3f896813187a0035611))

* Display splash in paginatesongs ([`6548f08`](https://github.com/mps-youtube/yewtube/commit/6548f08ab71cf2df07afbb9bb239cb8c402f1f41))

* Use .append() instead of += ([`58ebac7`](https://github.com/mps-youtube/yewtube/commit/58ebac79c58081193221a95ac38bfc717cf78e22))

* Use g.model.songs instead of g.model in generate_songlist_display() ([`ce2a2f3`](https://github.com/mps-youtube/yewtube/commit/ce2a2f3c8601c2e3186742a31cef224e7e1f9ebb))

* Correct &#39;rm all&#39; command ([`a0e347f`](https://github.com/mps-youtube/yewtube/commit/a0e347fbdb7466f0e25603accd8f148f44bd7f0f))

* Replace various instances of g.model.songs with g.model ([`369c1a0`](https://github.com/mps-youtube/yewtube/commit/369c1a09718a62147ceb12552fbb0ab51e85aff9))

* Correct user_pls for change in pl_search ([`bce9054`](https://github.com/mps-youtube/yewtube/commit/bce905486f7488fe29a9d68d2673a91a1a6f71dc))

* Use paginatesongs for the view command ([`ebbb86a`](https://github.com/mps-youtube/yewtube/commit/ebbb86af0bfa57a7b789970da1a885a34fca662d))

* Store keyword arguments in g.last_search_query ([`4687308`](https://github.com/mps-youtube/yewtube/commit/468730892305becb696780590977573488c887be))

* Simplify _search using new feature of paginatesongs ([`449d27e`](https://github.com/mps-youtube/yewtube/commit/449d27e2d0fddab5340238e6606fd6c1ee5a4c3c))

* Make paginatesongs take a slicable object as an alturative to a function ([`ae51ad9`](https://github.com/mps-youtube/yewtube/commit/ae51ad99038494da948597896903e0d1edb1102e))

* Add __getitem__ method to Playlist ([`12ed4e6`](https://github.com/mps-youtube/yewtube/commit/12ed4e6fe5b2c6cd2037f49254a6a714c8b1e355))

* Make preload thread a daemon ([`a2ed69a`](https://github.com/mps-youtube/yewtube/commit/a2ed69af40edadec6f87392407032e271180ba70))

* Use paginatesongs for handling local playlists ([`d78b124`](https://github.com/mps-youtube/yewtube/commit/d78b124a6750f98e116238c3d04ff2603456f9f8))

* Strip digits from start of playlist name using &#34;save&#34; ([`8befeb6`](https://github.com/mps-youtube/yewtube/commit/8befeb6b415e56a89b61a876c220a525926b2b7c))

* Remove trailing newline ([`0e06b19`](https://github.com/mps-youtube/yewtube/commit/0e06b197f02d5cbe763d063f98844ee8c575c6a3))

* Remove seemingly unnecessary test ([`b91e3eb`](https://github.com/mps-youtube/yewtube/commit/b91e3ebddd8ae597f6cc04d953bdbb6a6ba4fec7))

* Merge pull request #399 from mps-youtube/paginatesongs

[WIP] Use paginatesongs() for all search commands ([`fa39836`](https://github.com/mps-youtube/yewtube/commit/fa3983602c887ba7864f1c7e956e26bc14e03bc4))

* Fix download playlist command ([`9c0acc1`](https://github.com/mps-youtube/yewtube/commit/9c0acc11011a062b75322881f78d29ec3f57e158))

* Correct function name ([`663b080`](https://github.com/mps-youtube/yewtube/commit/663b080d450c3ee49441ed6938292841802357f1))

* Remove page argument to generate_search_qs ([`b0e154b`](https://github.com/mps-youtube/yewtube/commit/b0e154b8655d45bdc2b18782556c804d14118e06))

* Fix bug in search ([`979a938`](https://github.com/mps-youtube/yewtube/commit/979a938b4032a5ef14436a6dd495beda93927c77))

* Minor syntax simplification ([`5fb7c05`](https://github.com/mps-youtube/yewtube/commit/5fb7c05f888f3202403510f55e8e41e6ee619ad7))

* Remove no longer used dumps parameter of plist ([`cfe32d1`](https://github.com/mps-youtube/yewtube/commit/cfe32d1c4e6dd89527d00bed580d96786178b007))

* Use paginatesongs() in album_search ([`516bec8`](https://github.com/mps-youtube/yewtube/commit/516bec84d05a31071310baec13f4a75f9708595b))

* Fix album search ([`bbf8fa1`](https://github.com/mps-youtube/yewtube/commit/bbf8fa183af9988a7b02011e9ea8a9c40361b97c))

* Slight simplification ([`4efef7d`](https://github.com/mps-youtube/yewtube/commit/4efef7d1f60dbb71db3750fd5e25763ab5918401))

* Have msg and failmsg for paginatesongs ([`0a329fc`](https://github.com/mps-youtube/yewtube/commit/0a329fcfbadadb7656a771e6a1ccbbc5f009935f))

* Set g.last_opened() in paginatesongs() ([`706dcf7`](https://github.com/mps-youtube/yewtube/commit/706dcf740438bda44cc5614f448730e6d23946b7))

* Call generate_songlist_display() in paginatesongs() ([`e451f6e`](https://github.com/mps-youtube/yewtube/commit/e451f6edbb689f85b59d48e778e643d1d1761581))

* Remove unused frmt parameter of generate_songlist_display() ([`878fb54`](https://github.com/mps-youtube/yewtube/commit/878fb547289b5dbba7f91ebd750e91a8a455a263))

* Use paginatesongs() for searches (WIP) ([`f34ebf6`](https://github.com/mps-youtube/yewtube/commit/f34ebf6f103259f9db006fa68cc8190aebdb2334))

* Allways get 50 results for search ([`a807888`](https://github.com/mps-youtube/yewtube/commit/a807888fcd0123013865e08934861530e57b0058))

* Generalize pagination code used by plist()

This should then be used by other functions ([`1b8ca9f`](https://github.com/mps-youtube/yewtube/commit/1b8ca9fe0a725ae9046b352d91ef1fcfb98c7262))

* Remove unneeded temporary variable ([`849fdbc`](https://github.com/mps-youtube/yewtube/commit/849fdbc862bc613b12348f65fda5971afb9ec21f))

* Remove url_memo, no longer used since code was moved to pafy

There are better ways to cache data, but that really should then be
implemented before the next release ([`1286a88`](https://github.com/mps-youtube/yewtube/commit/1286a8814d41339490b16e188a3d255fdef8bfa4))

* Restructure some logic in nextprev() ([`8973318`](https://github.com/mps-youtube/yewtube/commit/8973318f91479d96af59051edc563d0c77a03752))

* Simplify definition of dump ([`42fa9f5`](https://github.com/mps-youtube/yewtube/commit/42fa9f5ffc486824386bc4aacec48a6efdc6554b))

* Change g.last_search_query format to (function, param) tuple ([`4633877`](https://github.com/mps-youtube/yewtube/commit/4633877e1200d0082e7bb21fdf394992a872d2c9))

* Set g.result_count and g.more_pages in search_album() ([`51e7846`](https://github.com/mps-youtube/yewtube/commit/51e78463847a83a7603175a1ce10541ee79e5ce7))

* Remove unused import ([`7a0815e`](https://github.com/mps-youtube/yewtube/commit/7a0815e7b5aea1eaf8a0e6feff26cc8dc5c7d920))

* Trivial simplification ([`bfcadd8`](https://github.com/mps-youtube/yewtube/commit/bfcadd8d23aa498d62b24e5f78129eb2f0af4c56))

* Replace Playlist.is_empty and playlist.size with __len__() ([`3e5ee46`](https://github.com/mps-youtube/yewtube/commit/3e5ee46030198b9a550926f8b4fdbb32a90e7e5e))

* Rename cache.init() to cache.load() ([`c7e052a`](https://github.com/mps-youtube/yewtube/commit/c7e052a3049814d17070ab8218106b3b11e9ef0c))

* Move import_config() to Config.load() ([`8e184d6`](https://github.com/mps-youtube/yewtube/commit/8e184d67d630181b884c585dc8f2f9713058690d))

* Create screen.msgexit() function for exiting with a message ([`925229b`](https://github.com/mps-youtube/yewtube/commit/925229bbbe244f3517896521448f372c41d404b4))

* Refactor version printing code; remove newlines at start and end ([`cd182a3`](https://github.com/mps-youtube/yewtube/commit/cd182a35cd83ca704bb18f86265767aca20a0d44))

* No longer align prompt to bottom and rest to top

I thought I already reverted this change... ([`cd5b3c4`](https://github.com/mps-youtube/yewtube/commit/cd5b3c466a05ede3e3656505d15ff3fa55febf8f))

* Merge branch &#39;get_playlist2&#39; into develop ([`d168478`](https://github.com/mps-youtube/yewtube/commit/d16847803a9695408dbe9a599426e2f21b7b48f2))

* Update install_requires for pafy get_playlist2() ([`4239f7b`](https://github.com/mps-youtube/yewtube/commit/4239f7b187a49c450c7cbe20b326e285f8d2c0a2))

* Fix dump command ([`25d05d1`](https://github.com/mps-youtube/yewtube/commit/25d05d1b33872e2e89c24e9e3e26947d2fe0a8ac))

* Fix dump for playlist ([`837a845`](https://github.com/mps-youtube/yewtube/commit/837a845c596cd2347fd207752ed125fd4206eed6))

* Load videos from playlist only as needed ([`82d0a34`](https://github.com/mps-youtube/yewtube/commit/82d0a3406f660e606e7b3c1efe4f7587d6133a44))

* Update get_playlist2() calls for change in API ([`b6065d5`](https://github.com/mps-youtube/yewtube/commit/b6065d5412e6ec84adbaa54f4f9a7460271ebf06))

* Import call_gdata and GdataError from pafy ([`73028df`](https://github.com/mps-youtube/yewtube/commit/73028dfbe8d87ce4318c73cc202ab18a607575c7))

* Update for change to get_playlist2() to namedtuple ([`056111b`](https://github.com/mps-youtube/yewtube/commit/056111ba75477c44ed24f29f20831b2baf2be59a))

* Use pafy.get_playlist2() ([`ec2f2e3`](https://github.com/mps-youtube/yewtube/commit/ec2f2e37d471bce820873253e0decfc22da60969))

* Correctly display extension when asking to mux audio ([`4c6ea97`](https://github.com/mps-youtube/yewtube/commit/4c6ea97b70c09501d13b55eaa9c7113a576337c1))

* Test for muxing based on mediatype, not extension

Fixes the feature, since the youtube_dl change in pafy changed the m4v
extension to the (more correct) mp4 ([`e526133`](https://github.com/mps-youtube/yewtube/commit/e526133268310106450a850168efe31d31e5e058))

* Merge pull request #394 from Wildefyr/develop

remove unneeded showconfig() argument ([`8d2c22d`](https://github.com/mps-youtube/yewtube/commit/8d2c22d7d1410a84cd98ec1f3a0270063770041f))

* remove unneeded showconfig() argument ([`25bc263`](https://github.com/mps-youtube/yewtube/commit/25bc263be1e7c177c46065fb3d2974b5afb6da74))

* Remove number_fmt functionality of F(), as well as unused argument

This functionality can be provided just as easily by the other notation,
was only used once, and seems unintuitive. ([`ea4831f`](https://github.com/mps-youtube/yewtube/commit/ea4831fc0868e53dd7ea3dec1fb478227a126fe3))

* Small simplifications to F() ([`5e3404c`](https://github.com/mps-youtube/yewtube/commit/5e3404c0dc3be4d6c364a9f683fc5980605896d6))

* Remove redundent definition of g.text ([`c37c501`](https://github.com/mps-youtube/yewtube/commit/c37c501e284c2ba302621c5c44b05dcdbbea6536))

* Use .fullmatch() for command regex matching; remove $ from end of each

They all were being used this way (except a couple that should have). If
the other functionality is needed for some reason, .* can just be added
to the end of the regex. ([`a9bd45d`](https://github.com/mps-youtube/yewtube/commit/a9bd45dfccd034355fcae4fc5d04f65c66ad1f57))

* Remove capture group from showconfig regex ([`5cb1024`](https://github.com/mps-youtube/yewtube/commit/5cb10245ab6e65584e09ee3fb434ff03c61e4cf9))

* Use .pop() in defining next_inp ([`729def0`](https://github.com/mps-youtube/yewtube/commit/729def007452b03dbd4045de28a9ed6f33e44ec2))

* Display playlist after running browserplay, instead of blank screen ([`08e98f3`](https://github.com/mps-youtube/yewtube/commit/08e98f31989851492fda2191360c64a7782e64e7))

* Merge remote-tracking branch &#39;rjvani/develop&#39; into develop ([`88f43d8`](https://github.com/mps-youtube/yewtube/commit/88f43d8dd0fb64323612e1d8bf280508787338da))

* Remove browsersearch functionality ([`ca40d17`](https://github.com/mps-youtube/yewtube/commit/ca40d177fa6f9902703b4de5c16f0c257efcd2cc))

* Update browserplay to use previous searches ([`9e011d8`](https://github.com/mps-youtube/yewtube/commit/9e011d842c137789ce2bd6b768adbfae07d89cc2))

* Searching for terms on YouTube in default browser ([`f689fda`](https://github.com/mps-youtube/yewtube/commit/f689fdad1780cf76a4ce45c23f3549c6e400ecce))

* Open YouTube URL in default browser ([`4035657`](https://github.com/mps-youtube/yewtube/commit/40356579179b6af506ebb73b5fb2432d01d343f7))

* A couple regex simplifications ([`fbc574f`](https://github.com/mps-youtube/yewtube/commit/fbc574fe9693047d4aee582c4b1b00287bee4693))

* Remove \s* from start and end of some command regexs

The command has already been stripped of whitespace, so this does
nothing ([`77fbc23`](https://github.com/mps-youtube/yewtube/commit/77fbc23b4c426b9d5a03a3c17e79008cc9e8be78))

* Append to data_files rather than replacing it (was in plugin branch) ([`dd8d50f`](https://github.com/mps-youtube/yewtube/commit/dd8d50f83ef3ab7a552380e67c92caed0c2b6405))

* screen_update -&gt; screen.update; clear_screen -&gt; screen.clear ([`c077fd0`](https://github.com/mps-youtube/yewtube/commit/c077fd07591fbd88d5f120437215cf8959ab566d))

* Fix pl regex

Lost in rebase ([`c944383`](https://github.com/mps-youtube/yewtube/commit/c9443837cf26575738bdb999d43bf9090029c296))

* Add g.commands

Was in plugin branch ([`40a55e2`](https://github.com/mps-youtube/yewtube/commit/40a55e2c353b08f5b5eeae6456fb8fcb8c32c8db))

* Change setup.py to properly install README, etc. ([`d5084c7`](https://github.com/mps-youtube/yewtube/commit/d5084c79ff4964f970e527b55d8955dac012419b))

* getxy()-&gt;screen.getxy() to work in plugins branch ([`83d2161`](https://github.com/mps-youtube/yewtube/commit/83d2161cf57e524a5a151170d2cf00eeb642f67b))

* Add screen.py, move some functions to it

This file should eventually have all uses of (x)print and
sys.stdout.write, so that it can redirect that to the UI, when multiple
are supported ([`aa245b1`](https://github.com/mps-youtube/yewtube/commit/aa245b12f4a58cc7c8b499882e5e327b1b3319d6))

* Use decorator to store command regex ([`db6882b`](https://github.com/mps-youtube/yewtube/commit/db6882b86be01e1799305ef413c3aa22ac8cede4))

* For url_file, ignore blank lines ([`cccbf08`](https://github.com/mps-youtube/yewtube/commit/cccbf0894172a738732715c1f8f876b0992e49f5))

* A couple modifications to url and url_file syntax ([`cd30803`](https://github.com/mps-youtube/yewtube/commit/cd308039883edf38b440d5b53cb28d7915d61578))

* use of &#39;with&#39; statement to open the file ([`b54c0f1`](https://github.com/mps-youtube/yewtube/commit/b54c0f17eeed99cf256494a717e787bc3fc2fd08))

* style corrections ([`665a835`](https://github.com/mps-youtube/yewtube/commit/665a835abf82eb939b9cd05110b3c6da445d5724))

* Import videos from a list of url, from console or text file ([`236472a`](https://github.com/mps-youtube/yewtube/commit/236472a3d75c0480013cc26087af6202cc6e621c))

* Merge pull request #385 from JKatzwinkel/develop

Fix right-aligned status line prompt when using colors. ([`885c351`](https://github.com/mps-youtube/yewtube/commit/885c351b9a3afb8b0ea34377d18c956fe5e33ea9))

* Drop local reassignment of builtin function.

Because apparently, that&#39;s considered bad practice. ([`59195a9`](https://github.com/mps-youtube/yewtube/commit/59195a9e75c9e2155aa3d0e9b82ad579c641ff19))

* More descriptive name for visible length function.

In color module `c`. ([`78a5544`](https://github.com/mps-youtube/yewtube/commit/78a5544eef1b3f359963d1b4cddf89255da826e9))

* Fix right-aligned status line prompt when using colors. ([`06dd919`](https://github.com/mps-youtube/yewtube/commit/06dd919d689ff00c9ca9eaa79ebea314f70d1e8e))

* Merge pull request #386 from oparkadiusz/patch-1

Added mpv player to Dockerfile ([`5d0d387`](https://github.com/mps-youtube/yewtube/commit/5d0d387e79e3c236af2d5502d3ab32e27d73e30d))

* Added mpv player to Dockerfile

For better support :) ([`4ffab40`](https://github.com/mps-youtube/yewtube/commit/4ffab40f581501dd24e9f118909d892894b597c1))

* Display warning when adding duplicate tracks to playlist ([`e63e2a9`](https://github.com/mps-youtube/yewtube/commit/e63e2a90fc20ab4f6b3bf55dbd0f33ab7532c1c9))

* Merge pull request #380 from wdv4758h/fix-main

Fix local variable &#39;mpv&#39; &amp; &#39;mplayer&#39; referenced before assignment ([`77c8b18`](https://github.com/mps-youtube/yewtube/commit/77c8b180d9c8aacae62adcf7fb1df333125bbafb))

* Fix local variable &#39;mpv&#39; &amp; &#39;mplayer&#39; referenced before assignment ([`419e922`](https://github.com/mps-youtube/yewtube/commit/419e922da23f7d542fe83f4314761f86c3c39156))

* Actually, don&#39;t use [:]; use copy.copy() ([`16e4596`](https://github.com/mps-youtube/yewtube/commit/16e45969928bc7aebb22014fa3652f03d3cca80a))

* Use [:] instead of .copy(), which was apparently added in python 3.3 ([`d587438`](https://github.com/mps-youtube/yewtube/commit/d5874380d2be34103be7c019c472a3e16f456020))

* Run import_config() before other things in init

This way those can use config settings ([`6b1bf1f`](https://github.com/mps-youtube/yewtube/commit/6b1bf1f1d4866f6ade8dc0839fa188bef8195e89))

* Allow external_download to get youtube id (with %i) ([`e05f997`](https://github.com/mps-youtube/yewtube/commit/e05f9977bc212e91de7ee43e8129a2594aae4265))

* Make streams.select() code saner ([`fcb88f6`](https://github.com/mps-youtube/yewtube/commit/fcb88f66e8400aaa72b359920efbc4b770011c43))

* Go back to clearing the screen with whitespace ([`ae810a4`](https://github.com/mps-youtube/yewtube/commit/ae810a44ea6a30cab29f8ccdf8e767a78c48842c))

* Revert &#34;Align prompt to bottom of screen&#34;

This reverts commit ca56aec7ed3d56066d42c57613784a4fe98ae8ab. ([`da26423`](https://github.com/mps-youtube/yewtube/commit/da264233c5ffdc199e429b7abf37352618c91523))

* Do not have stream.select() call stream.get()

On second thought, just keep the verbosity ([`88aa4ca`](https://github.com/mps-youtube/yewtube/commit/88aa4cae7c44ed3c4d755a1ae32a3f7e0c4b331f))

* Fix streams.select(), yet again ([`146d5e7`](https://github.com/mps-youtube/yewtube/commit/146d5e76bd56893c9afe42929a97b8e9af9f97ff))

* Show clearer error message on failure of user search ([`7ac16d1`](https://github.com/mps-youtube/yewtube/commit/7ac16d1d2faa8b8070b0b2148440befbc3dbb295))

* Do not cause UnboundLocalError on reaching retry limi ([`447462e`](https://github.com/mps-youtube/yewtube/commit/447462e1ec6b054e296b5b8d121aa1695167ab40))

* Do not pass unneeded parameter to streams.select() ([`f4ca354`](https://github.com/mps-youtube/yewtube/commit/f4ca3541f4f97ac2e5ac8c0a9ac126eb13e39ae8))

* Fix bugs from having streams as both local and global

Also make first arg of stream.select() optional ([`c1b922f`](https://github.com/mps-youtube/yewtube/commit/c1b922f71a8053ee3ff24ed5f374e35fbaadd94d))

* Fix typo in README ([`725b0be`](https://github.com/mps-youtube/yewtube/commit/725b0becd631e9137b6453287f4d75c74d954ff6))

* Revert &#34;Move playlist save/load functions to playlist.py&#34;

This reverts commit 5c149e87a8fa40cfa85ebea88fa9f5e9941df6db. ([`0e78cb1`](https://github.com/mps-youtube/yewtube/commit/0e78cb15504229844f0b60d8d1477a025ff4f062))

* Revert &#34;Make open_from_file call convert_playlist_to_v2&#34;

This reverts commit b216dcc163991265b8ce71a1e43d0190472fd23b. ([`6e6f941`](https://github.com/mps-youtube/yewtube/commit/6e6f941d4f8faa5903f4ac1ab18e559280ae0836))

* Make open_from_file call convert_playlist_to_v2 ([`b216dcc`](https://github.com/mps-youtube/yewtube/commit/b216dcc163991265b8ce71a1e43d0190472fd23b))

* Move playlist save/load functions to playlist.py ([`5c149e8`](https://github.com/mps-youtube/yewtube/commit/5c149e87a8fa40cfa85ebea88fa9f5e9941df6db))

* Deal with bug in pafy before 88fda70 or 0.7.x ([`275a538`](https://github.com/mps-youtube/yewtube/commit/275a5383ab8f481396bf9cfe7d66646bc9533838))

* Fix issues caused by incorrect search and replace ([`7f6afa0`](https://github.com/mps-youtube/yewtube/commit/7f6afa0c1510116a8420264f7cbf04038917bde9))

* Move cache and streams code into seperate files ([`7b59b29`](https://github.com/mps-youtube/yewtube/commit/7b59b29790a0892b896cdcf9acdfa6eafbf00317))

* Fix bitrate sorting of audio; also changes cache format

Do not depend on order of streams, which was changed accidentally in the
last pafy release. The required a change to the format of the stream
cache, so versioning of the cache is added and old versions are not
used. ([`7c9f9eb`](https://github.com/mps-youtube/yewtube/commit/7c9f9eb42264f98b038adfb46f02e50ca99670cd))

* Merge pull request #338 from hrnr/mpris-fix

catch all dbus exception in mpris ([`b6b3b60`](https://github.com/mps-youtube/yewtube/commit/b6b3b6063e57926b3d4bbecadf3d2b1883d70192))

* catch exceptions on dbus initialization

error reporting: error msg will be simply printed out ([`412ec86`](https://github.com/mps-youtube/yewtube/commit/412ec86952e65309fec63476f1f330470306381c))

* catch all dbus exception in mpris

since mpris is not critical, rest of the mps-youtube can run with no problems

fixes #337 ([`defe2a9`](https://github.com/mps-youtube/yewtube/commit/defe2a99536904178161d745f820f30f914a963c))

* Merge pull request #352 from TimoDritschler/forcevid

Made -v play option force video as configured ([`f4435e8`](https://github.com/mps-youtube/yewtube/commit/f4435e8c1158b918d62badc275e8c2d5001eb171))

* Made -v play option force video as configured

-v used to do the same as -w which was a bit awkward.
-v now forces video playback according to the options set in the config
and still gives precedence to the -w and -f options ([`83eaea7`](https://github.com/mps-youtube/yewtube/commit/83eaea7d6335b40c0ef65c56652699049eadf1cc))

* Fix definition of not_utf8_enviornment ([`d884326`](https://github.com/mps-youtube/yewtube/commit/d884326fa5826f722da200bff81efbe52c7ed85e))

* Use &#34;import sys&#34; rather than &#34;from sys import stdout&#34; ([`4879481`](https://github.com/mps-youtube/yewtube/commit/487948112717fb4d83df12c4190fca531c1f669d))

* Merge pull request #349 from livingBEEF/develop

Use terminal control sequences only on terminals ([`121a0f6`](https://github.com/mps-youtube/yewtube/commit/121a0f6977d1c10b11ab9cc2081e4677fc71d0be))

* Use terminal control sequences only on terminals ([`e1a403b`](https://github.com/mps-youtube/yewtube/commit/e1a403be5a2c9fc8ae619c3a7f02938421d22ab7))

* Fix youtube playlist matching regex to accept urls ([`0788f98`](https://github.com/mps-youtube/yewtube/commit/0788f9837af6e58e33a2498cd3f0a535ef2c68bf))

* Replace playlist regex with the one from pafy

Fixes matching of mixes ([`a9fbe15`](https://github.com/mps-youtube/yewtube/commit/a9fbe156ddcd6622b435cf7cec2f8f0e366e7642))

* Allow sorting by title ([`81d802a`](https://github.com/mps-youtube/yewtube/commit/81d802aa546d433baa31e6ebb9ee733064eecfdd))

* Simplify writeline and integrate it into writestatus function

It seems the spaces it was adding were unnecessary... ([`dad497a`](https://github.com/mps-youtube/yewtube/commit/dad497a3a5230a7f5ed969273cea8d972f05a2fe))

* Prevent endless loop when truncating to negative length

Still some improvement to be done ([`b6eb0d8`](https://github.com/mps-youtube/yewtube/commit/b6eb0d862798dfd8f53df4ff05544073fd73c7a4))

* Merge pull request #339 from hrnr/notifier

do not wait for notifier ([`a585b98`](https://github.com/mps-youtube/yewtube/commit/a585b98f591265e654e9a216e2a2e534d5cff424))

* do not wait for notifier

this allows notifier to do some more complex operations without causing delay in playback. ([`a04e53d`](https://github.com/mps-youtube/yewtube/commit/a04e53d5b0788c367bca429740352445e8e424f1))

* Merge pull request #336 from Evidlo/develop

Changed the mplayer version regex ([`e66e43b`](https://github.com/mps-youtube/yewtube/commit/e66e43bb6dba0753626c1c579959036fec15519a))

* Changed the mplayer version regex so that the following two Mplayer version strings match successfully

MPlayer svn r34540 (Debian), built with gcc-4.7 (C) 2000-2012 MPlayer Team
MPlayer SVN-r37391-5.1.1 (C) 2000-2015 MPlayer Team ([`42f2520`](https://github.com/mps-youtube/yewtube/commit/42f252043c975b54ef60fc0e3b919be7533150cb))

* Remove GdataError handling in fetch_comment() ([`fc6a690`](https://github.com/mps-youtube/yewtube/commit/fc6a6907ad7d09a762120a38adeddc2bb3bbe54a))

* Fix handling of GdataError ([`9f9679f`](https://github.com/mps-youtube/yewtube/commit/9f9679f416dbaf3a6237189b20acf66af321e8b4))

* Use shields.io since pypip.in seems to be down ([`65dd797`](https://github.com/mps-youtube/yewtube/commit/65dd7977118c88a5f7b01a1e6a2a6f527810903c))

* Remove special case in xenc() for non-tty use ([`2f3754d`](https://github.com/mps-youtube/yewtube/commit/2f3754d2641f8dda0d3677be91184e8374520138))

* Fix issue with &amp; in titles on windows ([`0b103fc`](https://github.com/mps-youtube/yewtube/commit/0b103fc40fabd05089b3642197389975f1c04a90))

* Change screen.getxy()-&gt;getxy() so it will work in current develop branch ([`79f1232`](https://github.com/mps-youtube/yewtube/commit/79f1232e00d821de0341edde0d72ce19bb0c1ad1))

* Fix error in page-switching after playlist download ([`27e1363`](https://github.com/mps-youtube/yewtube/commit/27e13634138056170131628662d73641395d3a43))

* Make `down_plist` download entire playlist

Change behaviour of `plist` when called with `dumps` flag so that playlist
downloads are no longer limited to the videos displayed in their first result
page. This should fix issue #294. ([`5c4f704`](https://github.com/mps-youtube/yewtube/commit/5c4f7041ad32df7ee0513849ceda414530dc4daf))

* Use mpv.com instead of mpv.exe on windows

Fixes some issues ([`f28761c`](https://github.com/mps-youtube/yewtube/commit/f28761c8617b24600d51d719930f71f9cf0f8e3e))

* Make xenc always return string rather than bytes

Fixes TypeError when trying to print to the screen ([`e9516ef`](https://github.com/mps-youtube/yewtube/commit/e9516ef5ed35a8dc462f0373cec6ff067a60b24d))

* Fix typo in variable name that broke argument parsing ([`ceb7e1d`](https://github.com/mps-youtube/yewtube/commit/ceb7e1dcc36e090675ce03f80d7fedd13ac43edf))

* Merge pull request #317 from paddatrapper/develop

Changed error message to advise updating mplayer ([`3228193`](https://github.com/mps-youtube/yewtube/commit/32281933e158c005db0e2a101ff64561d3f72f7e))

* changed error message to advise updating mplayer ([`a67c3af`](https://github.com/mps-youtube/yewtube/commit/a67c3afa0ac1768e5747d647a7819634660084c7))

* Revert &#34;Make setup.py derive version from __version__&#34;

This reverts commit c920b91b1d74e986e9853fe8d73937046f19b832.

This broke installs when pafy was not installed. ([`76a16d0`](https://github.com/mps-youtube/yewtube/commit/76a16d099c9ea0cc9081f955833e210f381ee219))

* Check if mplayer recent enough to support https ([`4126439`](https://github.com/mps-youtube/yewtube/commit/4126439d5d0457178ddb187fd1887d32291e2081))

* Remove commented out code

The functionality is needed, but has been moved elsewhere ([`16e1a48`](https://github.com/mps-youtube/yewtube/commit/16e1a48ca049106f680f635ffc317256d501b0cb))

* Add &#39;del _Config&#39; so more instances cannot be created ([`5ea817b`](https://github.com/mps-youtube/yewtube/commit/5ea817bd5e369ea77b015a637ce3ad51079ba88c))

* Move more help logic into helptext.py; more functions into util.py ([`88e8ddf`](https://github.com/mps-youtube/yewtube/commit/88e8ddf4020a643d0fd27b157807220daf0a6c84))

* Move helptext into it&#39;s own file

Fixes use of globals in helptext; allows for more dynamic help (like
when plugins are implemented) ([`b528867`](https://github.com/mps-youtube/yewtube/commit/b5288674288d153fcfd4b9cd7b2e9b85c9e64d9e))

* Remove redundancy in ConfigItem name definition

Better not to have redundancy; should help for implementing config items
in planned plugin api ([`b36a342`](https://github.com/mps-youtube/yewtube/commit/b36a34264a7668cec216af9444d62b79ecfda030))

* Remove debian directory ([`31bf0aa`](https://github.com/mps-youtube/yewtube/commit/31bf0aa1d1b5826436496657cb08e33726412c3f))

* Remove unused imports ([`655d935`](https://github.com/mps-youtube/yewtube/commit/655d935e9f1cdbe1a98293b324d1469259114396))

* Remove g.text definition into g.py; remove init_text() function ([`a7fa1c2`](https://github.com/mps-youtube/yewtube/commit/a7fa1c29aef911a9b31d75303c8089949da0fd10))

* Move a couple functions out of main.py ([`5684dac`](https://github.com/mps-youtube/yewtube/commit/5684dacb5d65e871f73137ab811a2fe781026757))

* Remove __future__ import from main.py ([`dc88cc6`](https://github.com/mps-youtube/yewtube/commit/dc88cc6e604c50c0dbc39fd1a22c09fcf541f205))

* Fix pylist misplaced_future ([`aa6e43f`](https://github.com/mps-youtube/yewtube/commit/aa6e43ffc8848ddb3b6de37a251a9a8a4bc7f540))

* Move landscape compat code to where it is needed ([`c628914`](https://github.com/mps-youtube/yewtube/commit/c628914188d174e3f4b888f0757e894622c6a915))

* Remove __name__ == &#39;__main__&#39; test in main.py

Serves no purpose; there is no reason this module would be called a
script ([`bf3e6c5`](https://github.com/mps-youtube/yewtube/commit/bf3e6c5a7b68201e0647cc3fb7c3a7f0b01a0e45))

* Split into more files ([`af5c0b0`](https://github.com/mps-youtube/yewtube/commit/af5c0b0a2413c645d202d2d3a3a9959f90e24149))

* Remove g.COLOURS

It&#39;s value is currently ignored, and it&#39;s use in c is causing trouble
splitting the code into files ([`0ed75e1`](https://github.com/mps-youtube/yewtube/commit/0ed75e14f9fb3f2c3fb5e75b4d6f0b061ad4e5ac))

* Fix --debug; make no_clear_screan block extra newlines in screen_update ([`534dd4c`](https://github.com/mps-youtube/yewtube/commit/534dd4c3f228ef178c541248f3f5b3f37af4fb61))

* Use argparse to handle arguments ([`ef76410`](https://github.com/mps-youtube/yewtube/commit/ef764106489695a120383600b7ba4a0a408fc8bd))

* Move saveconfig to Config.save() ([`c140d62`](https://github.com/mps-youtube/yewtube/commit/c140d6213aa57e6e1d59bc4e7207d9278d354113))

* Store ConfigItems in OrderedDict; add Config.__getitem__ function ([`475725b`](https://github.com/mps-youtube/yewtube/commit/475725bd0232e59b40d44bde669e87e71685ba5b))

* Make allowed_values and require_known_player parameters of...

ConfigItem.__init__ ([`3083b44`](https://github.com/mps-youtube/yewtube/commit/3083b44c50709e2558eca80d21d1e460d3ced720))

* Fix Config.__iter__ by making Config is Singleton class instance ([`8b4f6da`](https://github.com/mps-youtube/yewtube/commit/8b4f6dacc94b4fb19608e3acc453f0dc89698c87))

* Move Video to playlist.py ([`d4bda9e`](https://github.com/mps-youtube/yewtube/commit/d4bda9eab4784e77a42f1af1ca8bf2d612c68bc2))

* Split out a few parts of the code into files ([`bac2ebd`](https://github.com/mps-youtube/yewtube/commit/bac2ebdab5a6bf6d8dde87b57d774ca46ef88513))

* Use is not None rather than !=; use ternary rather than bool index ([`cda498b`](https://github.com/mps-youtube/yewtube/commit/cda498bcc81c7cc25d39fd1c716768c946dba448))

* A couple random code simplifications ([`cfd457d`](https://github.com/mps-youtube/yewtube/commit/cfd457d0cacba61b4d9343fe94e1fe14f6e8e292))

* Remove unused g.defaults ([`5d368cc`](https://github.com/mps-youtube/yewtube/commit/5d368cc84cb0fdf17ea596464ffbc8357b3b76e4))

* Fix bug with blank g.content ([`3504c47`](https://github.com/mps-youtube/yewtube/commit/3504c471d717aa644210aa9a97ac1e0357265d25))

* Align prompt to bottom of screen ([`ca56aec`](https://github.com/mps-youtube/yewtube/commit/ca56aec7ed3d56066d42c57613784a4fe98ae8ab))

* Add py2exe excludes for pyperclip ([`508875d`](https://github.com/mps-youtube/yewtube/commit/508875d0c785acabac56ed939d73a99e549fcc63))

* Use os.system instead of subprocess.call for cls

It is part of the shell, not a binary ([`4d621a2`](https://github.com/mps-youtube/yewtube/commit/4d621a2c1c67ae736d188a2d9fa020136fd148c7))

* Clear screen with cls/tput reset instead of blank lines (#239) ([`38b257d`](https://github.com/mps-youtube/yewtube/commit/38b257d51aceb8800930cd145d673cd02dfaeeb9))

* Update version to 0.2.6-dev ([`133de9b`](https://github.com/mps-youtube/yewtube/commit/133de9b942848885b7e963020d54e8a4fe719703))

* Remove rothgar/ from docker example ([`8395aba`](https://github.com/mps-youtube/yewtube/commit/8395aba2e469f6ae6d80217f4ab3e10de83bc642))

* Merge remote-tracking branch &#39;rothgar/docker_container&#39; into develop ([`dd8170c`](https://github.com/mps-youtube/yewtube/commit/dd8170ceadc00beab497de38dde77d0cdb26c684))

* comma :sob: ([`4398a31`](https://github.com/mps-youtube/yewtube/commit/4398a31099357371e230b7a3b5c45d9685e2de18))

* updated rst formatting ([`c1feabb`](https://github.com/mps-youtube/yewtube/commit/c1feabbc946cc1cf5e6a13ac03d0da8ba4c2c699))

* Added a Dockerfile and information to README ([`2c64e06`](https://github.com/mps-youtube/yewtube/commit/2c64e0651a33e0fb59d3283a409f6274eeee71f7))

* Add pafy to .gitignore ([`43eaeed`](https://github.com/mps-youtube/yewtube/commit/43eaeedc0006d820ca3cb04c910332d8ff882be2))

* setup.py: Only try to import py2exe on Windows ([`e528531`](https://github.com/mps-youtube/yewtube/commit/e528531018569adb3d269869002700bbd861e673))

* Use pyperclip module instead of unmaintained and broken xerox ([`0e3a9ca`](https://github.com/mps-youtube/yewtube/commit/0e3a9ca0b9cfa575b8a5d0030eb1bfe9d661c67c))

* Make setup.py exit with error when run in python 2 ([`0f83e42`](https://github.com/mps-youtube/yewtube/commit/0f83e42951a49871a550e4305429081cca35174d))

* Make setup.py derive version from __version__ ([`c920b91`](https://github.com/mps-youtube/yewtube/commit/c920b91b1d74e986e9853fe8d73937046f19b832))

* Merge pull request #310 from stephenbalaban/bugfix/py2exe

Fixed linux installation bug (py2exe related) ([`f512bd7`](https://github.com/mps-youtube/yewtube/commit/f512bd7c2ae3e5e98a9634842b9f10bacbd712d0))

* Fixed linux installation bug (py2exe related)

Also cleaned up tab/whitespace issues in setup.py

Setup.py is now pep-8 compliant.

Previously, this error was being thrown after importing py2exe:

File &#34;/usr/local/lib/python3.4/dist-packages/py2exe/_wapi.py&#34;, line 4, in
&lt;module&gt;

      _kernel32 = WinDLL(&#34;kernel32&#34;)

      NameError: name &#39;WinDLL&#39; is not defined

This happened on my Ubuntu 14.04 LTS system. ([`d162d2a`](https://github.com/mps-youtube/yewtube/commit/d162d2aaf1e43d380898a6b2757c60db006239dc))

* Remove more old pafy compatibility code ([`4effcec`](https://github.com/mps-youtube/yewtube/commit/4effcecbe36617418f098e9c32d35ad2c8459b50))

* Remove compatibility code for old pafy

Only the most recent version of pafy is supported due to other changes,
so this serves no purpose. ([`252bb1e`](https://github.com/mps-youtube/yewtube/commit/252bb1e75dacb8ab4117bd2378455b477d14812d))

* Use Config.PLAYER.set instead of redefining Config.PLAYER on first run ([`292180c`](https://github.com/mps-youtube/yewtube/commit/292180c1b7d18897ef4162d12ffb3332a9fb0535))

* Merge branch &#39;develop&#39; of github.com:np1/mps-youtube into develop ([`4cc964a`](https://github.com/mps-youtube/yewtube/commit/4cc964a9fb242bfd88106834a4267276dc3d40eb))

* Merge pull request #306 from zgrimshell/develop

debian revision updates ([`bfa7cd2`](https://github.com/mps-youtube/yewtube/commit/bfa7cd29f0b65af391a8505d65a78d64665cd704))

* debian revision updates ([`2d9eb7c`](https://github.com/mps-youtube/yewtube/commit/2d9eb7ceb9f62ba62e53c3f22b5e3d1fbdd92d91))

* Add MANIFEST.in to include desktop file in sdist archive ([`f5f63ce`](https://github.com/mps-youtube/yewtube/commit/f5f63cecd7eb99bfe2096445c01a7ff47050db2a))

* Correct rst syntax ([`6a33edf`](https://github.com/mps-youtube/yewtube/commit/6a33edfeda7678c9f7848afd0f565a19ad42a09c))

* Add note about standalone binary to README.rst ([`5258f27`](https://github.com/mps-youtube/yewtube/commit/5258f27ccd0579746e59f2c3628f326eeaf6af5f))

## v0.2.5 (2015-06-01)

### Unknown

* Merge pull request #301 from zgrimshell/develop

Updated debian directory ([`7e457d2`](https://github.com/mps-youtube/yewtube/commit/7e457d2b4700387b88a3c96579e13cb76ca1f06b))

* use pybuid in debian ([`56a4620`](https://github.com/mps-youtube/yewtube/commit/56a4620709b1189c350855f2d8b021095e6c64ea))

* Updated debian ([`2c4fc52`](https://github.com/mps-youtube/yewtube/commit/2c4fc5270c1d12bebc85ddd1be070c93e9f66d02))

* Update contributing for no python 2 ([`e2cf7cf`](https://github.com/mps-youtube/yewtube/commit/e2cf7cf8557d5b708264570bfc7c7d07b73b2b70))

* Update CHANGELOG ([`d05ca9d`](https://github.com/mps-youtube/yewtube/commit/d05ca9deebed62645c205f1006fd73a76b9e302f))

* Version 0.2.5 ([`02ffd3b`](https://github.com/mps-youtube/yewtube/commit/02ffd3bd0a14d4b61ec799cae7d2083e2bff2671))

* Update CHANGELOG ([`40cc2c3`](https://github.com/mps-youtube/yewtube/commit/40cc2c3d9c8ee3903e47cc7c7c8f3064d71d6c6c))

* Make default &#39;user_order&#39; blank, and make that the same as &#39;order&#39; (#293) ([`078ab5e`](https://github.com/mps-youtube/yewtube/commit/078ab5e0f968f121d64687ffe8e1373c438eb1af))

* Fix UnicodeEncodeError in subprocess.Popen call ([`6bf017d`](https://github.com/mps-youtube/yewtube/commit/6bf017d64f8efd3242f27200ece90404cf64536d))

* Update setup.py trove classifiers for py3 only ([`47d71ab`](https://github.com/mps-youtube/yewtube/commit/47d71abb3361b33853ea28a8a69d2615b861f557))

* Fix bug in xenc() ([`f37193a`](https://github.com/mps-youtube/yewtube/commit/f37193a00a48ab93778e978a22c1ab72caeadf05))

* Remove incorrect .decode()

This worked with utf8_decode() (althogh that shouldn&#39;t have been there) ([`858a365`](https://github.com/mps-youtube/yewtube/commit/858a365a4c5a5d71df0427e97e83ec2afdc2f904))

* Remove unnecessary parentheses ([`60a0ce6`](https://github.com/mps-youtube/yewtube/commit/60a0ce6eba82a27b85743102b05a6d43f908ee14))

* Remove utf8_encode() and utf8_decode()

Perhaps these functions were needed when python 2 was supported (not
sure) but it should by possible to do without them now. ([`8376db0`](https://github.com/mps-youtube/yewtube/commit/8376db07a675afbfe093efe59c3e01dc17716154))

* Do not need to store output of sys.stdout.isatty() in variable ([`fa5290e`](https://github.com/mps-youtube/yewtube/commit/fa5290e6b948cf3416ab9945150d69de27453e8d))

* Fix width when unsuported characters are replaced with ? ([`b0901db`](https://github.com/mps-youtube/yewtube/commit/b0901db02cad66a1a1164a28e873ad01dac9d192))

* Reorder imports following pep8 guidelines ([`7f48ba5`](https://github.com/mps-youtube/yewtube/commit/7f48ba5fe4168cdf37d15c94fa62992c844a06f3))

* Replace if with elif ([`577657a`](https://github.com/mps-youtube/yewtube/commit/577657a9a4332d05c0604283bb23788ddea0d0d0))

* Move mps-youtube.desktop to root directory ([`22c567c`](https://github.com/mps-youtube/yewtube/commit/22c567ca91f4a8e7b3fccc00a054f901cb965a34))

* Merge pull request #289 from hrnr/desktop-file

Reworked desktop file install ([`5ecddbd`](https://github.com/mps-youtube/yewtube/commit/5ecddbdd54819fffb9e54113a25aa07b184c36c9))

* revert installing desktop file at runtime ([`ceaaa9c`](https://github.com/mps-youtube/yewtube/commit/ceaaa9cc62db6189c6ca8ddbd7703a9957253e24))

* install desktop file via setup.py ([`2df485a`](https://github.com/mps-youtube/yewtube/commit/2df485adaa56351746ed0cafb16ec9f06790c2d6))

* Remove setup.cfg setting to universal wheel

Now py3 only ([`99736ae`](https://github.com/mps-youtube/yewtube/commit/99736ae1cab1d3c37aa5d7d481f66213e41c5f16))

* Fix g.more_pages value; remove redundant generate_songlist_display() ([`ea2e41a`](https://github.com/mps-youtube/yewtube/commit/ea2e41a6cb67058781d1507ff3fd7a3881e70950))

* Replace while loop with arithmetic ([`f2fcd27`](https://github.com/mps-youtube/yewtube/commit/f2fcd27113b869c941bb454f2e7c32841fe51259))

* Remove redundant page number display ([`aaf4db6`](https://github.com/mps-youtube/yewtube/commit/aaf4db63a2673b436be66c5837912ef8b074901a))

* Merge branch &#39;pagination&#39; of https://github.com/JKatzwinkel/mps-youtube into develop ([`6fdb267`](https://github.com/mps-youtube/yewtube/commit/6fdb2675f7923443573ca766c08cd842f618ee83))

* Fix page count bug, update page/result number assumption in plist. ([`7a6a9d8`](https://github.com/mps-youtube/yewtube/commit/7a6a9d811bee400fdda1294b3718e4aeb4d7e2b6))

* fix another error due to unassigned variable ([`effd117`](https://github.com/mps-youtube/yewtube/commit/effd1179e50e1d868d0053ab609fccc4c5c5bdce))

* Merge remote-tracking branch &#39;jkatzwinkel/pagination&#39; into develop ([`aa30c6f`](https://github.com/mps-youtube/yewtube/commit/aa30c6ffc9a9e23d4594c7b7d38a7faf59db5819))

* Fix error with uninitialized g member ([`d1e0357`](https://github.com/mps-youtube/yewtube/commit/d1e0357b35bb4ae02183af46e95b995b352dd5d3))

* Fix type error in page status msg ([`030f4ae`](https://github.com/mps-youtube/yewtube/commit/030f4ae2ada60a801b08654cd26c67e2b1d7114f))

* Fixed bug in album search caused by pagination fix. ([`b045feb`](https://github.com/mps-youtube/yewtube/commit/b045feb06a06c99288408c541841ae5dca87065a))

* code style compliance ([`d04f4a5`](https://github.com/mps-youtube/yewtube/commit/d04f4a5e0c4ce77637561d6f098f02ac17b890b7))

* Add optional command parameter.

If a page number is given with the `p` command, the search result page at the
specified position will be opened. ([`0ff7c9e`](https://github.com/mps-youtube/yewtube/commit/0ff7c9e1e931f70aad02d7038d94b8913263c60f))

* Fix tiny error in search mode switching. ([`5820d0e`](https://github.com/mps-youtube/yewtube/commit/5820d0ed9aaed5fb32ead79772e75f69dc2cfea3))

* Display pagination info in status line.

If a video or playlist search yields more results than can be listed with the
current terminal size, the page number currently opened and the total number
of pages are shown in the bottom-right corner in the status message line. ([`d7fdd83`](https://github.com/mps-youtube/yewtube/commit/d7fdd83f604404c11d66cbd9384ee16c1dc71da9))

* Methods to utilize search result count info for pagination.

Added methods for extracting search result count and pagination
data from json, and for formatting current page information.

With the total amount of search results present, it can be determined
how many pages of search results can be made available to the user
(considering the current terminal size).

Note: New API limits the number of search result items it provides to the
first 500. ([`744f4c3`](https://github.com/mps-youtube/yewtube/commit/744f4c3c832663f80dbdbee0f85ea55516662462))

* Fix, standardize pagination, make independent from token list.

Pagination is finally consistent throughout mpsyt search methods/
API versions. Should be more robust and more flexible.

  * Drop extracted page token list, generate page tokens ourselves.
	* Go back to numeric page parameter for all search methods; potential
	  for optional page parameter in mpsyt search commands
	* Page counter now starts at 0, easier to handle ([`ab57955`](https://github.com/mps-youtube/yewtube/commit/ab57955e925553ba152e10cec408842ba2ac686d))

* Do not call pafy.set_categories(); generic caching code already exists ([`8828bf5`](https://github.com/mps-youtube/yewtube/commit/8828bf5f5f1df8b42b80d0d7900457f043d39f40))

* Merge branch &#39;develop&#39; of https://github.com/JKatzwinkel/mps-youtube into develop ([`403cfc7`](https://github.com/mps-youtube/yewtube/commit/403cfc7d1497ef430a349df89d655135b2d3283a))

* Remove / adjust code to work with upcoming Pafy release

Pafy will henceforth handle category name resolution, so this doesn&#39;t need
to be implemented in mpsyt anymore. ([`661f08d`](https://github.com/mps-youtube/yewtube/commit/661f08d21efdcf10e46cad86d8e432a65744e485))

* Save and load pafy cache ([`7bf43b5`](https://github.com/mps-youtube/yewtube/commit/7bf43b56618088df177a782c5f7d3cf2cf42ba51))

* Run tests if test_main executed as script ([`23a3dff`](https://github.com/mps-youtube/yewtube/commit/23a3dffe364c092e25ee1c34ffab6a20ebcf6cb7))

* Make Video arguments non-optional

Unused; would result in crash anyway due to int(None) call ([`78ef337`](https://github.com/mps-youtube/yewtube/commit/78ef3372dbb4b7d4c52b9cbbb30e4fea2c8a386c))

* Install destop on systems other than Ubuntu; other improvements

Testing for Ubuntu specifically is a hack, while the file does not harm
on other systems and could be of use there too. ([`8c9254e`](https://github.com/mps-youtube/yewtube/commit/8c9254e9bfecc1102628563163d0788812250af0))

* Merge remote-tracking branch &#39;origin/ubuntu-desktop-file&#39; into develop ([`8ee8444`](https://github.com/mps-youtube/yewtube/commit/8ee844479744380cff2f21a56bb93ee04a16bcf1))

* correction to docstring comment ([`752a0fd`](https://github.com/mps-youtube/yewtube/commit/752a0fd73c5d9c48dbe1d895efe17ef37f2ffabb))

* Install desktop file on first run on Ubuntu systems ([`def138c`](https://github.com/mps-youtube/yewtube/commit/def138c3571b2417604a97e2caf272ec7ed68a11))

* Fix slight inconsistency in code style ([`17b6e9d`](https://github.com/mps-youtube/yewtube/commit/17b6e9d3c85944cd4bfc5dc7b465583cfe643751))

* Make channelfromname() give a better error message ([`83c0b49`](https://github.com/mps-youtube/yewtube/commit/83c0b49ce776de91c305447f84e595239cddc274))

* Remove time.sleep() in match_tracks()

Seems unneeded; faster obviously ([`a3350cc`](https://github.com/mps-youtube/yewtube/commit/a3350ccf42136f6601fb5909dbd7c85312ad992d))

* Inline add_to_url_memo() since it&#39;s used only once; add docstrings ([`9efa037`](https://github.com/mps-youtube/yewtube/commit/9efa03734b1d88a7db747fe8b865cc9ffb36896a))

* Better error messages for gdata; remove some duplication of code ([`dcbe6f7`](https://github.com/mps-youtube/yewtube/commit/dcbe6f79ae15dbf954787298d6bf3d662f0cfd7f))

* Remove distutils support; setuptools required

If build with setuptools, the mpsyt script will depend on setuptools.
It is probably easier to just not support distutils at all. ([`3cd9024`](https://github.com/mps-youtube/yewtube/commit/3cd9024f96f44246b6c74473cac8737c9ca0ca6c))

* Revert &#34;Fix distutils support&#34;

This reverts commit 4ef23efbc09504e975ee0e2ac058c418e112f436. ([`1925373`](https://github.com/mps-youtube/yewtube/commit/1925373b3c5d449dfdea8f56db57145fb753db69))

* Revert &#34;Fix error in setup.py&#34;

This reverts commit a9c67d4d22217590dcb5027cdbc06d332b354605. ([`ad07b67`](https://github.com/mps-youtube/yewtube/commit/ad07b6721090caa7a250f79b0fc251c0a350fdca))

* Fix error in setup.py ([`a9c67d4`](https://github.com/mps-youtube/yewtube/commit/a9c67d4d22217590dcb5027cdbc06d332b354605))

* Merge branch &#39;develop&#39; of https://github.com/JKatzwinkel/mps-youtube into develop ([`8b509d9`](https://github.com/mps-youtube/yewtube/commit/8b509d9d102ecafe80a4826e4b70929a24c31529))

* fix bugs in result displays and satisfy isse #244 ([`9ea2ee7`](https://github.com/mps-youtube/yewtube/commit/9ea2ee74a73efd7ad20be799f723c76ee05de835))

* Fix result page change bug.

Fix bug which caused crashing on last result page of result sets
whose total number of items amount to multiples of max_results.
Also fix minor issue in pagination initialization. ([`1c24a70`](https://github.com/mps-youtube/yewtube/commit/1c24a704ca9eaf8cef1fbf7e9c4f20c36e79d789))

* Fix page caching in playlist search results.

Save list of playlist Ids to cache when searching
for playlists. This enables using cached results when
changing to a known search result page which we already
evaluated an API call for. ([`743a18f`](https://github.com/mps-youtube/yewtube/commit/743a18f208dbf5872a55d9255039a84924ab8ef7))

* Fix result number argument in playlist retrieval query ([`1f81aac`](https://github.com/mps-youtube/yewtube/commit/1f81aac8dbfbad3feab32f030302044618efb26f))

* remove line breaks in display list item titles ([`c4682e0`](https://github.com/mps-youtube/yewtube/commit/c4682e0b4a218be48f52fe6059a582627ee794ad))

* Fix distutils support ([`4ef23ef`](https://github.com/mps-youtube/yewtube/commit/4ef23efbc09504e975ee0e2ac058c418e112f436))

* Fix issue with // and search_music (#282) ([`5549e80`](https://github.com/mps-youtube/yewtube/commit/5549e80bdfb9c3f0eace71e8d539c2c0a15e94e0))

* Fix indentation ([`02a5df8`](https://github.com/mps-youtube/yewtube/commit/02a5df882f6dd5e4305cbb681f3d92b76d9d37f0))

* try/except in mix() ([`e8e7921`](https://github.com/mps-youtube/yewtube/commit/e8e79210f1951c4e63202bf535719dfae9d42b5e))

* Remove debug code ([`537b436`](https://github.com/mps-youtube/yewtube/commit/537b4364bc9a17adb63714d3069664f062562cb7))

* Merge branch &#39;develop&#39; of github.com:np1/mps-youtube into develop ([`7def56a`](https://github.com/mps-youtube/yewtube/commit/7def56a92b8afe83045ddf8053f973c79d9b518b))

* Merge pull request #281 from hrnr/landscape_fix

fix landscape bot ([`e67f40e`](https://github.com/mps-youtube/yewtube/commit/e67f40e69476916d883df8cd911a5adeb7c95f9e))

* fix landscape, be python2 friendly ([`2c74185`](https://github.com/mps-youtube/yewtube/commit/2c7418551072d9dd1fa311f80be54772c1e0cfa2))

* Merge category fixes from &#39;np1/develop&#39; ([`9c8457a`](https://github.com/mps-youtube/yewtube/commit/9c8457a9a0481acc0347b634fe429455ee1e9e2c))

* Extend time after which category cache expires to two days. ([`d3fc734`](https://github.com/mps-youtube/yewtube/commit/d3fc734735b5401f73b0854b83898614bf9621a2))

* Add YouTube mix command ([`2ef61ca`](https://github.com/mps-youtube/yewtube/commit/2ef61ca6f76c07d3c906ced386a28b43e1e9da77))

* Use shields.io pypi badge ([`113be2a`](https://github.com/mps-youtube/yewtube/commit/113be2afb2223f8c4556d821c1dd80ffc8f2e2f1))

* Remove code unneeded due to removal of initial category_names ([`e236c49`](https://github.com/mps-youtube/yewtube/commit/e236c496bd92efb9968e693c37a0d97da6d598fb))

* Remove predefined category_names

Unneeded; should fix bug due to difference in format between original
dict and generated one ([`d0e403b`](https://github.com/mps-youtube/yewtube/commit/d0e403bebcd084f208faf2f1387841e5b3350c2f))

* Remove landscape.io badge for now

Now working with python3 ([`9e6657c`](https://github.com/mps-youtube/yewtube/commit/9e6657c6b741233c76c2f5c5887d9b0d1f36c11d))

* Add more py2exe excludes ([`6e8be13`](https://github.com/mps-youtube/yewtube/commit/6e8be13ee1cb826e4c93c059941c2d27a5b92603))

* py2exe without warnings ([`b1a5b71`](https://github.com/mps-youtube/yewtube/commit/b1a5b71e2578fdccd623e1fb8738b85a1d9eca10))

* Fix writeline() on windows ([`67f2326`](https://github.com/mps-youtube/yewtube/commit/67f232645f95fd45e8e728fc1d65b090f7c1b4e0))

* Revert &#34;Fix terminal size on Windows #215 #223&#34;

This reverts commit 8e139d9b1f6841f66fd729620236002927133ba3. ([`fbd028e`](https://github.com/mps-youtube/yewtube/commit/fbd028edc4d5fe67a3ce8df3f47e7bdd23b26ab7))

* Make i command show category title instead of id ([`88c7436`](https://github.com/mps-youtube/yewtube/commit/88c743665623e28cea0ad6c812978be31d64c10a))

* Merge branch &#39;develop&#39; of https://github.com/JKatzwinkel/mps-youtube into develop ([`b471699`](https://github.com/mps-youtube/yewtube/commit/b4716990164d2d8157125e6a8a36470efcd5dabc))

* Query API for unknown or expired video categories

  * check known categories for expiry on startup
	* call API on any unknown category coming in with json search results
	* save category list to cache file and load on startup ([`f55abd6`](https://github.com/mps-youtube/yewtube/commit/f55abd6157f1a8091a87ff4abca0e3a4c738ee60))

* Fix error in video duration extraction from json

Regex had to be fixed to match ISO8601-formatted durations
that drop seconds field because of whole hour/minute. ([`fd3662f`](https://github.com/mps-youtube/yewtube/commit/fd3662fd4dfa588258a7e5384e4dd6457e5f6989))

* Fix tiny issue with video categories ([`3ab04c5`](https://github.com/mps-youtube/yewtube/commit/3ab04c5e53c2a3fec8ee5217922b0a1b90bed8e4))

* Merge remote-tracking branch &#39;np1/develop&#39; into develop ([`e0b7112`](https://github.com/mps-youtube/yewtube/commit/e0b711213b71de997358dbe97303e9ae7d9631c6))

* Merge remote-tracking branch &#39;np1/develop&#39; into develop ([`20e033d`](https://github.com/mps-youtube/yewtube/commit/20e033d89cbbec4a634e5a10757b55f2a9a20d79))

* Merge remote-tracking branch &#39;np1/develop&#39; into develop ([`a34d631`](https://github.com/mps-youtube/yewtube/commit/a34d631c2d4d476ae0b736bae142f3a2d0981fa6))

* Merge v0.2.4 from branch &#39;np1/develop&#39; into develop

And fix keyerror in search result display generation on playlist search
related to changes in video category retrieval. ([`0f17b5c`](https://github.com/mps-youtube/yewtube/commit/0f17b5cecce7b2486877ecd65fc97d6b9b9f80a8))

* Merge playlist search changes from &#39;ids1024/gdata3wip&#39; ([`aa34d75`](https://github.com/mps-youtube/yewtube/commit/aa34d751407c4aca3a7f66e4f48c78bf69642236))

* remove fixme in album search method ([`4dbc1e2`](https://github.com/mps-youtube/yewtube/commit/4dbc1e22b6b5e7709ed69e062a718c13f4d09278))

* fix some code style concerns linter had ([`2ba7e82`](https://github.com/mps-youtube/yewtube/commit/2ba7e82fec396dc06dc3cdb33e672ce0570f060b))

* make &#39;u &lt;num&gt;&#39; command invoke fitting method ([`1c5cb62`](https://github.com/mps-youtube/yewtube/commit/1c5cb629f282b9c72bff41e341c9a4366252a52d))

* Map video category names to Ids ([`77baf14`](https://github.com/mps-youtube/yewtube/commit/77baf141df24b9b674c357eae325c2ecc6e63aeb))

* Do not check mpv version if not installed ([`08c3798`](https://github.com/mps-youtube/yewtube/commit/08c37986023bd7f12f2d789b8fb8e5de541177cb))

* Merge pull request #277 from lol768/develop

Separate search order for user uploads ([`622c21b`](https://github.com/mps-youtube/yewtube/commit/622c21b08dd570ed670c6af1ac86916a394ac02a))

* Separate search order for user uploads ([`6db1ce5`](https://github.com/mps-youtube/yewtube/commit/6db1ce5f70e6a79fa3b0a960fadec70da3bb7d80))

* Set pafy api_key ([`17d847e`](https://github.com/mps-youtube/yewtube/commit/17d847ec7c0816bae3aac74d806f56395248d7a3))

* Fix UnicodeEncodeError with logging to ascii console ([`f2305f9`](https://github.com/mps-youtube/yewtube/commit/f2305f93850e7d949b09eba237855a60a694b776))

* Use xenc in set_window_title ([`0b5be5d`](https://github.com/mps-youtube/yewtube/commit/0b5be5d7604bad239ee802659fdaba2819c7a1ce))

* Fix playlist parsing ([`2eef024`](https://github.com/mps-youtube/yewtube/commit/2eef024bc7730e678670d0e7359e4e8b104eff4a))

* Do not use py2 compatabile u&#34;&#34;

Does not work in earlier py3 versions; unneeded ([`0ffd79f`](https://github.com/mps-youtube/yewtube/commit/0ffd79faf3cd5b11687861e3d75c9b513a0e7ab1))

* Merge pull request #272 from lol768/patch-1

Add mention of IRC channel to README ([`d339780`](https://github.com/mps-youtube/yewtube/commit/d339780fecc64a0fc6f9c5bd84483c728fbe5d38))

* Add mention of IRC channel to README ([`418e203`](https://github.com/mps-youtube/yewtube/commit/418e2032499a04f94a3bdb03724b083a37eab533))

* Merge pull request #269 from zgrimshell/develop

Debian directory (with changelog) ([`faaf12d`](https://github.com/mps-youtube/yewtube/commit/faaf12d4e9d1f8e6cbe96ab1fc8f30c3173a31e9))

* remove changelog from gitignore ([`d073eed`](https://github.com/mps-youtube/yewtube/commit/d073eed41b8a1558d25d718933a09679110be04f))

* Merge remote-tracking branch &#39;upstream/develop&#39; into develop
Incorporating latest upstream changes so I can prepare fresh Debian package ([`39a1619`](https://github.com/mps-youtube/yewtube/commit/39a16199faaa4c1f7023d00a39407d4bdddc93a8))

* Debian directory ([`172d1fc`](https://github.com/mps-youtube/yewtube/commit/172d1fcc8acc280bff118fd231ba2ad20974f7f9))

* Update README for python 3 only ([`3f7c992`](https://github.com/mps-youtube/yewtube/commit/3f7c9928d98625c2c98234d707f866e2df49450b))

* Remove __future__ import

No longer supporting python 2 ([`c5fb3fa`](https://github.com/mps-youtube/yewtube/commit/c5fb3fa86c7a5d4740f4cc89e3332776a731a9c3))

* Use shutil.get_terminal_size() if python recent enough ([`b23c91b`](https://github.com/mps-youtube/yewtube/commit/b23c91bb074d31057b05b29e88f78a9fe39f57af))

* Fix terminal size on Windows #215 #223

Don&#39;t know if the +1 was there for a reason... ([`8e139d9`](https://github.com/mps-youtube/yewtube/commit/8e139d9b1f6841f66fd729620236002927133ba3))

* Remove #! from library py files ([`e13df6c`](https://github.com/mps-youtube/yewtube/commit/e13df6cc7d61b2b5c05441de574ca3ced348b3c8))

* Merge pull request #251 from psachin/remove-quotes

Remove double-quotes from filename if any. ([`c06f3da`](https://github.com/mps-youtube/yewtube/commit/c06f3daf176fae8e56518adaad01cf5ddf2cb39b))

* Remove double-quotes from filename if any.

Having double-quotes in filename makes it difficult to play(manually) in
terminal using cli players like &#39;mplayer&#39;. Better remove the quotes
before saving the file. ([`21a5e56`](https://github.com/mps-youtube/yewtube/commit/21a5e567cf67302371772787f4d8a85889d3cb0b))

* Merge pull request #252 from punchagan/init-set-mpv-version

Check mpv_version on startup. ([`8e01fef`](https://github.com/mps-youtube/yewtube/commit/8e01fef59a6b14d05b06bdca1b713a6a9b59a6b7))

* Check mpv_version on startup.

`mpv_version` is not saved to config, and not set correctly when mpsyt
is restarted after setting player to `mpv`. ([`7e15de8`](https://github.com/mps-youtube/yewtube/commit/7e15de83cbe8f44305b22d2a1d56fa8a3569a603))

* Update version to 0.2.5-dev ([`cc1b775`](https://github.com/mps-youtube/yewtube/commit/cc1b775ee42eaaf8b31ceb857b2a2478d6393028))

* Use python 3 explicitly in #!&#39;s ([`4d4a3c3`](https://github.com/mps-youtube/yewtube/commit/4d4a3c3fe04978ad6c4973ab2093b675007d3dc4))

* Drop python2 support ([`8575efa`](https://github.com/mps-youtube/yewtube/commit/8575efa0e71b04a3a43b79f88b3dfd104efe251b))

## v0.2.4 (2015-05-13)

### Unknown

* Version 0.2.4 ([`582d203`](https://github.com/mps-youtube/yewtube/commit/582d2034b844f15815867d840cfa976d1f66b0a7))

* Update CHANGELOG ([`c478f6c`](https://github.com/mps-youtube/yewtube/commit/c478f6c85f4aa97ae7869505dae26ab5fe982181))

* Change default api key ([`032cca9`](https://github.com/mps-youtube/yewtube/commit/032cca94bc6fc30f9a1130e3112fcb4ad2782d42))

* Use gdata3 for playlist searches ([`ce06ed8`](https://github.com/mps-youtube/yewtube/commit/ce06ed8cbd08af02962fa2c0ed30652346fa4d80))

* limit username search term cache size, as done with streams cache ([`22c4b22`](https://github.com/mps-youtube/yewtube/commit/22c4b227e9d62e200d588f2850a60bf876f35135))

* pickle username query cache alongside stream cache ([`e5dbc4b`](https://github.com/mps-youtube/yewtube/commit/e5dbc4b68819f17dfca46f1d4761b4dcbee2f079))

* Fixed lookup issue in switching to a previously loaded result page

because page tokens in search responses need to be handled carefully,
cached query lookup on page switching did not lead to performance advance
until loading and caching cached page a second time. Now this is fixed. ([`c144ca7`](https://github.com/mps-youtube/yewtube/commit/c144ca760ef15fc77f7b7bfb4568217f3f742d90))

* Worked on code style to make pylint/landscape happy ([`62b40b1`](https://github.com/mps-youtube/yewtube/commit/62b40b180f8c2d6f27cfb4c6fcfc9e3c72e41d40))

* Try to use cached user data on user uploads search

usersearch caches resolved username and channel id under provided username
search string. Next time a similar search string is passed to user search by
name, cached data is used rather than sending another api request. ([`90819c1`](https://github.com/mps-youtube/yewtube/commit/90819c18e080700009fea891972d487487a803be))

* fix encoding error in python2.7, usersearch query fallback ([`f2c6362`](https://github.com/mps-youtube/yewtube/commit/f2c636295402c79c7a0f9f770b436d5c891af031))

* Improve uploaded video search by user name

Change query for uploaded video search for given user name to `search` API
endpoint as it returns more/better channel matches than `channel` queries.
Response is used to retrieve both channel id and channel title (user name)
matching search string so that we get nicer status messages. ([`c279fc2`](https://github.com/mps-youtube/yewtube/commit/c279fc22848850ebd79174cf166c29257591c8fd))

* Handle user not found search error ([`55bb239`](https://github.com/mps-youtube/yewtube/commit/55bb239eab1a364e2eb6f01338aedfcab9e0c4dc))

* Merge pagination fix changes from &#39;lol768/gdata3wip&#39; ([`88b84a4`](https://github.com/mps-youtube/yewtube/commit/88b84a48a5e04cac00f052ae42f42312376bc06b))

* Try and fix pagination for user searches. ([`e92af1d`](https://github.com/mps-youtube/yewtube/commit/e92af1d8773e8f309875b3ea7b3ad376741bd345))

* Working on video search result pagination ([`a7db186`](https://github.com/mps-youtube/yewtube/commit/a7db186a9d0fda9fda2accdf947fff936c93cc4e))

* Fix usersearch failmsg ([`ef445ee`](https://github.com/mps-youtube/yewtube/commit/ef445ee3a1cc0870a6aff3d88b420d85f4a7f4e7))

* Fix usersearch results message ([`329b576`](https://github.com/mps-youtube/yewtube/commit/329b576c63f54d289852f26355b12ac6d932eedc))

* Remove unnecessary variable ([`4f54405`](https://github.com/mps-youtube/yewtube/commit/4f54405d9e964676a564fb9fc6c387c40c6cca49))

* Correct user command searching status message ([`5a11052`](https://github.com/mps-youtube/yewtube/commit/5a110525f52c69e50595c95cdd0c945ca35db40c))

* Simplify usersearch() and filter geoblocked videos ([`aaa9a1a`](https://github.com/mps-youtube/yewtube/commit/aaa9a1a9952a9dacba00bc0df01349890339d773))

* Use config item for API_KEY in user uploads search

I believe this function wasn&#39;t present when I made the key configurable. ([`bdbfc98`](https://github.com/mps-youtube/yewtube/commit/bdbfc98569d91b37a226203119e5f948778f956b))

* Merge branch &#39;gdata3wip&#39; of https://github.com/lol768/mps-youtube into gdata3wip ([`113fc45`](https://github.com/mps-youtube/yewtube/commit/113fc45288ec1173b0c8c702b3eb1a3765f4c16c))

* Make api_key a config option

The purpose of this is to ensure users can use their own key if the main key ceases working or the quota is exceeded. ([`7616572`](https://github.com/mps-youtube/yewtube/commit/76165720b739686ff94d88dc75fef8973f143a62))

* Merge remote-tracking branch &#39;ids1024/gdata3wip&#39; into develop ([`f580fe7`](https://github.com/mps-youtube/yewtube/commit/f580fe710228908d177a9fd3cf028748282b6196))

* Disable safe search, like in the gdata2 version ([`e70bc9f`](https://github.com/mps-youtube/yewtube/commit/e70bc9f76f665355abd10de747687c2982754c08))

* Fix album search gdata3 ([`38e2ebc`](https://github.com/mps-youtube/yewtube/commit/38e2ebc892e02186b90c16fe22ad3a70d5c3cb29))

* Ignore Exuberant ctags tag file ([`4a17a41`](https://github.com/mps-youtube/yewtube/commit/4a17a4164de31a9e40e7870a727e810e72eeb143))

* Fix some output errors I accidentally created ([`624ad3e`](https://github.com/mps-youtube/yewtube/commit/624ad3e4982a01171a8abd2dc87d530ebe5e28ee))

* Comply project code conventions and tidy up a bit ([`4401879`](https://github.com/mps-youtube/yewtube/commit/4401879cd6b6d10a22588ccd80904e904f552e01))

* Make method usersearch method work with API v3

Reenables the commands `user &lt;username&gt;`, `user &lt;username&gt;/&lt;query&gt;`.
`usersearch` method has a new optional parameter `identify` by which
it can be specified whether a user is to be looked up by their channel
id or by their screen name. ([`ba4b474`](https://github.com/mps-youtube/yewtube/commit/ba4b47457fe47103a1cb82b0b41165d9409a4edb))

* Hopefully fixed bug in videoId extraction ([`e3fa018`](https://github.com/mps-youtube/yewtube/commit/e3fa018fc0fa875168677b5277f5bbf1da35b2ba))

* Get several features to work with Youtube API v3

Reactivated operations bound to keys r (related videos),
u (uploads by user) and c (show comments) by updating API
calls from v2 to v3.
Page navigation in search results, related videos, etc.
has been improved but still needs to be finished. ([`218925e`](https://github.com/mps-youtube/yewtube/commit/218925ef5c94e24e4612ef5ef6c263fc981dc5ab))

* Update standard video search API calls from v2 to v3

This fixes normal search. Few things to note:
API v3 requires API key and grants limited quota. Insert API key in line 119 in main.py.
New API does not provide all the expected information without using a second request.
So for each search, there is now an additional API call, potentially slowing stuff down. ([`42bc063`](https://github.com/mps-youtube/yewtube/commit/42bc06374488c645f7ca23e6757f73eb33a965f6))

* Merge pull request #247 from punchagan/fix-dumb-term-size

Use LINES and COLUMNS for termsize of dumb terminals ([`1f1b8ec`](https://github.com/mps-youtube/yewtube/commit/1f1b8ecfc98761ab3c72c6f563a21e46a9e1a97a))

* Use LINES and COLUMNS for termsize of dumb terminals

Using `fcntl.ioctl` returns (0, 0) termsize on a dumb Emacs terminal,
but &#39;LINES&#39; and &#39;COLUMNS&#39; environment variables give the correct size. ([`f917132`](https://github.com/mps-youtube/yewtube/commit/f91713208c1d04413a9559662b90f787fa5a2af8))

* Merge pull request #236 from ids1024/develop

Fix errors about trying to access methods of NoneType / sockpath not found ([`e0ccf11`](https://github.com/mps-youtube/yewtube/commit/e0ccf11ee9b55a23b0810fbed298109308c122d7))

* Don&#39;t try to unlink socket if it doesn&#39;t exist ([`4a7fbd8`](https://github.com/mps-youtube/yewtube/commit/4a7fbd870575e76cbdf9a4abe2c37d2eadb3598b))

* Fix errors about trying to access methods of NoneType ([`d13f315`](https://github.com/mps-youtube/yewtube/commit/d13f3155b7b8d900e647937b5d800621e81ea0cc))

* Merge pull request #229 from ids1024/develop

Set window title ([`6e3176a`](https://github.com/mps-youtube/yewtube/commit/6e3176a02814b525bf807a2acdfcb0fb982d7060))

* Set window title ([`c6c2b6b`](https://github.com/mps-youtube/yewtube/commit/c6c2b6b5caaf125313d0b749a3676a0145ca9c7f))

* Merge pull request #224 from ids1024/develop

Do not test mpv version during initialization ([`2471d24`](https://github.com/mps-youtube/yewtube/commit/2471d24e6b9dc5c4e8d84a4e69f704968b9bd236))

* Do not test mpv --input-unix-socket output on Windows ([`9c72c9a`](https://github.com/mps-youtube/yewtube/commit/9c72c9ac08b0c9f612a9e7a913adc5858c27127e))

* Do not test mpv version on initialization ([`c018ca5`](https://github.com/mps-youtube/yewtube/commit/c018ca5219275e15e1d8e565cdcae44402d99dcb))

* Replace generic text in instructions ([`0abcaf0`](https://github.com/mps-youtube/yewtube/commit/0abcaf0141f303400673b10f4ae60af7cc618f5d))

* remove list() ([`5865999`](https://github.com/mps-youtube/yewtube/commit/5865999ca8db2672df85b502140565b1b4672b42))

* Merge branch &#39;develop&#39; of https://github.com/np1/mps-youtube into develop ([`7818ff3`](https://github.com/mps-youtube/yewtube/commit/7818ff3a2500c7ad7a7522f2b66b6438cdc8df60))

* Merge pull request #219 from ids1024/develop

Some Minor Cleanup ([`4e0f0ed`](https://github.com/mps-youtube/yewtube/commit/4e0f0ed41110a3d0e4054c25036749d28aac25b7))

* Fix typo in docstring ([`3f096f9`](https://github.com/mps-youtube/yewtube/commit/3f096f9708faaa4c6f5c11ad4c289272c18df18f))

* Simplify a line ([`727707a`](https://github.com/mps-youtube/yewtube/commit/727707a2cfd6e6b81a79fa212c78599dbc8ab7b3))

* Use list.extend instead of while loop ([`14e2e88`](https://github.com/mps-youtube/yewtube/commit/14e2e885913a104628bfef88a2e0a85e9be5388e))

* update version number for dev ([`42559f7`](https://github.com/mps-youtube/yewtube/commit/42559f7291d21b39aac2aafc55b407ce85f8559d))

* fix typo ([`d1ec28f`](https://github.com/mps-youtube/yewtube/commit/d1ec28fb0d53566210194ded8c9ee2a14575eb9d))

* Fix opener syntax #217 ([`48f12de`](https://github.com/mps-youtube/yewtube/commit/48f12de2278e582de06778fe95b0ed07270687df))

* Documented changes ([`df6045e`](https://github.com/mps-youtube/yewtube/commit/df6045ebdfa8e115cef044bd35ff1c65483295f1))

* Use custom user-agent for musicbrainz requests #217 ([`ef5966c`](https://github.com/mps-youtube/yewtube/commit/ef5966c0943c7156015e94312708a5eaa849d688))

* Don&#39;t print more text than width #215 ([`6924081`](https://github.com/mps-youtube/yewtube/commit/6924081887de4bbdaf7acef57634d7f46c967da3))

* Don&#39;t print too many spaces #215 ([`8e42764`](https://github.com/mps-youtube/yewtube/commit/8e427642770a7e54c5deaf6d5e784b8e1e04cb5c))

* Merge branch &#39;mpris&#39; into develop ([`ff89a40`](https://github.com/mps-youtube/yewtube/commit/ff89a4028f86bfd812544e9713bfdbc64cdf560d))

* revert unneeded changes #210 ([`810c507`](https://github.com/mps-youtube/yewtube/commit/810c507524554c6b4073e05c5d7130770add2720))

* tidy ([`6e0bf53`](https://github.com/mps-youtube/yewtube/commit/6e0bf531cd79fb617162e0b38c04025931f65cff))

* add mpris arturl ([`f211a3d`](https://github.com/mps-youtube/yewtube/commit/f211a3d2e3a93885050de049b91d80ae3ce0b687))

* include mpris:artUrl ([`e3620a0`](https://github.com/mps-youtube/yewtube/commit/e3620a08d2f1ecb248bec5de5b6d15cc01c5612f))

* Add DesktopEntry for Ubuntu ([`a5913f3`](https://github.com/mps-youtube/yewtube/commit/a5913f335aed5bc27489e76381e31a1fa500a883))

* Merge branch &#39;develop&#39; into pr210

Conflicts:
	mps_youtube/main.py ([`25d956b`](https://github.com/mps-youtube/yewtube/commit/25d956ba2842d45927777d306737be0525a4093d))

* Merge branch &#39;hrnr-mpris&#39; into develop ([`f7c8c61`](https://github.com/mps-youtube/yewtube/commit/f7c8c617de5203b4bfa1b38f8d04d017f668ad3d))

* Merge branch &#39;mpris&#39; of https://github.com/hrnr/mps-youtube into hrnr-mpris

Conflicts:
	mps_youtube/main.py ([`59a44a5`](https://github.com/mps-youtube/yewtube/commit/59a44a57570b77c9853f2f6a7ff1519846637872))

* improve seeking

Seeking may cause time mismatch between mpris client and player time-pos if
seeking takes too long. This sends another signal when seeking finished to
ensure that time-pos will be synchronized properly (works only with mpv &gt;0.7). ([`7e7d131`](https://github.com/mps-youtube/yewtube/commit/7e7d1317a52bae8b0b632864e6735f64821f95e3))

* keep identity user-friendly

+ protect bus name from collisions (as required by specs) ([`ac17719`](https://github.com/mps-youtube/yewtube/commit/ac1771974b950641d951057c6762fbecb509a51f))

* changed licence
MIT is wrong as the project uses GPL
included hashbang ([`df03e85`](https://github.com/mps-youtube/yewtube/commit/df03e85cb921fd5ece156c7bbfc59414e264c688))

* fixes remaining landscape issues ([`bd83a10`](https://github.com/mps-youtube/yewtube/commit/bd83a1092762bb507dc458f243b6a2429f09afc2))

* dbus.service on some occurences couldn&#39;t guess dbus signatures from empty lists ([`d2a27f1`](https://github.com/mps-youtube/yewtube/commit/d2a27f12a07bd2409d578ffc6c2d9ee988a07a21))

* fixes various issues reported by landscape bot ([`cb55927`](https://github.com/mps-youtube/yewtube/commit/cb55927820511e072ea761b4847835f8ace0ae89))

* improved documentation ([`318310f`](https://github.com/mps-youtube/yewtube/commit/318310f8c00cb3fa687e529bfd9d0481d58649fb))

* Revert &#34;polished commands sending, should workk with old and new mpv and mplayer&#34;

This reverts commit 6872c236988e6871119a16f1d2972aa46ce5bf46.

Mplayer docs says pause property is read-only. Proper way is to send pause command. ([`90e3eb5`](https://github.com/mps-youtube/yewtube/commit/90e3eb59bf918177d45ce0bd1bcae3e7dc190462))

* polished commands sending, should workk with old and new mpv and mplayer ([`441ccdd`](https://github.com/mps-youtube/yewtube/commit/441ccdda70a1d2af9b7393899c45f7ed61424eed))

* Use &#34;pause&#34; to play or pause mplayer ([`16007ab`](https://github.com/mps-youtube/yewtube/commit/16007abf019eb70a6a1058f0aaf770fa33a83e29))

* Use &#34;cycle pause&#34; and &#34;pause&#34; to toggle pause in mpris ([`8273fc4`](https://github.com/mps-youtube/yewtube/commit/8273fc422e0bc76caa234a46ed023c97c4e78457))

* Initial support for mpris with mpv&lt;0.7 ([`3af6338`](https://github.com/mps-youtube/yewtube/commit/3af63383ce9b7d6fdff9acc4cd88a845f98c6f9f))

* Make KeyboardInterrupt set mpris status to Stopped ([`abb3cc4`](https://github.com/mps-youtube/yewtube/commit/abb3cc457b1578f3955508778b24a3266fc12d4e))

* Append .instancePID to mpris identity

The mpris standard says to do something like this when multiple
instances of a player can be run. ([`5f1c5c4`](https://github.com/mps-youtube/yewtube/commit/5f1c5c42f7a7bdd8b01c899a368842dfb68bdf62))

* restart event loop on keyboard interrupt ([`0d68495`](https://github.com/mps-youtube/yewtube/commit/0d684950cbbe3be72ed1d553a487ae312c3cc2f4))

* deals with race condition on observing properties (initial change event)
waits on socket properly in mpris ([`c092908`](https://github.com/mps-youtube/yewtube/commit/c092908544270ae1b4c99595090a3b7505dedb17))

* Fix mpris for volume=0 ([`26b5acc`](https://github.com/mps-youtube/yewtube/commit/26b5acc00be334d68f0fe72a4fefa4bd343259e9))

* implemented proper metadata
* title
* length
* using sanitized youtube id as object path
this will allow proper seeking, since seeking without knowing the length is problematic is most mpris clients ([`912fc28`](https://github.com/mps-youtube/yewtube/commit/912fc28c0ec60c8ff6fcd2292496a4ea135ff72f))

* removed supported uri schemes, since we don&#39;t support OpenUri ([`9438137`](https://github.com/mps-youtube/yewtube/commit/9438137baf6a31c7d6bbf0f111c0d6332fd3c5d3))

* fixed volume control (sometimes set as int), volume control now works properly with mplayer ([`abdd4e7`](https://github.com/mps-youtube/yewtube/commit/abdd4e7440747d4fb90548f0179b44b5830b1674))

* renamed temp file, since name was semantically wrong ([`e208502`](https://github.com/mps-youtube/yewtube/commit/e20850213c75375917a183a16c8034126ee47b1d))

* clean up that italian cuisine we had in communication protol to mpris process ([`26ea2d4`](https://github.com/mps-youtube/yewtube/commit/26ea2d45ab9d027bd73f3e09e25a9cc2ed925d71))

* setting volume now works (not tested for mplayer) ([`6ace4b7`](https://github.com/mps-youtube/yewtube/commit/6ace4b795008e3cb62912dc81db76882302e5acd))

* removed optional properties, since we are not implementing them yet ([`7764426`](https://github.com/mps-youtube/yewtube/commit/77644265448a8cb63db0280c416dae215b903f9a))

* implemented seeking ([`4fdd5a7`](https://github.com/mps-youtube/yewtube/commit/4fdd5a70a70b38b8916b059fc1766cdb1faa09df))

* implemented volume and time-pos properties, all properties sends signals properly ([`2b26999`](https://github.com/mps-youtube/yewtube/commit/2b26999edcc06b4b60d11cb56409208b2a78ca00))

* fixed pause query for mplayer (+ sending info only when needed) ([`98609f2`](https://github.com/mps-youtube/yewtube/commit/98609f28230c83682bdd13303f9954f6d29a6f13))

* Fix volume query for mplayer ([`86ea43b`](https://github.com/mps-youtube/yewtube/commit/86ea43b068797a7790f630a36d91fdb79f4073cf))

* Mark as stopped in mpris after stopping mplayer ([`25cae21`](https://github.com/mps-youtube/yewtube/commit/25cae216248128e479c9fee0399def7a0b1d7d06))

* basic support for mplayer (using fifo) ([`1936359`](https://github.com/mps-youtube/yewtube/commit/1936359596f2bcd3060518715f7f77501a8bfca7))

* Make mpris status work with mplayer/old mpv

Other functionality not yet implemented ([`96af1e5`](https://github.com/mps-youtube/yewtube/commit/96af1e5b980aadd2ba4e526fea8ef920c4983e59))

* Set mpris status to Stopped when player is stopped ([`7befd9c`](https://github.com/mps-youtube/yewtube/commit/7befd9ce3c4f8636f287e989cf7f5b8a0bc00a98))

* Fix mpris import ([`8de540f`](https://github.com/mps-youtube/yewtube/commit/8de540f4d8e35e3f290ac1f760c602c103b0d554))

* reworked, now using proper IPC to communicate
* horrible hack reverted, now interface is properly integrated
* works only with mpv &gt;= 0.7.0 (using unix socket to communicate)
* works with both python2 and python3
* requirements python-dbus and python-gi ([`69fa19f`](https://github.com/mps-youtube/yewtube/commit/69fa19f621643f3c816b33e22a00f746d30f2551))

* modified launching to run as single process
* releasing dbus resources properly ([`bc464d5`](https://github.com/mps-youtube/yewtube/commit/bc464d577b644a33a7722749c4f3d38684b7c0c7))

* Initial implementation of mpris wrapper
* dbus
* python 3
* xdotool
* glib ([`1405d48`](https://github.com/mps-youtube/yewtube/commit/1405d48b93d3b5d901aae3312f784fda14a1cc87))

* tidyup ([`ba812b3`](https://github.com/mps-youtube/yewtube/commit/ba812b3935f7714568458a00d80b98b032e4c961))

## v0.2.3 (2015-02-17)

### Unknown

* set version to 0.2.3 ([`69fa71c`](https://github.com/mps-youtube/yewtube/commit/69fa71c79e617fff663fcb80d41c12ec4a408f72))

* Update changes for v0.2.3 ([`0387e15`](https://github.com/mps-youtube/yewtube/commit/0387e15c566851a66ff0dedcf839154959cddb7e))

* open and repair old playlist file #214 ([`f20a523`](https://github.com/mps-youtube/yewtube/commit/f20a523b7025d062f81536a5a5106161f6bad24b))

* Implement rudimentary support for tagging audio files (#209)

This requires ffmpeg/avconv and implements tagging for downloaded audio files
when not using an external downloader application

This is quite basic, if a video is titled &#34;one two - three four&#34;, the artist is
assumed to be &#34;one two&#34; and the title &#34;three four&#34;

Otherwise the entire YouTube title is set as the title tag and no artist tag is
set ([`a96393c`](https://github.com/mps-youtube/yewtube/commit/a96393c1a5ab49a5e7019722c1b976407e305f0f))

* Fix typo in set config pattern match

set command currently ignores &#34;s&#34;&#39;s at end of command! ([`b8fe1a9`](https://github.com/mps-youtube/yewtube/commit/b8fe1a9edf294d0fc06207f2ac436680e2d7c707))

* Allow -v in place of -w for windowed mode (#213)
-v may be more intuitive ([`febe1ba`](https://github.com/mps-youtube/yewtube/commit/febe1ba083fac438fcbfa5f393251392e0925894))

* lowercase pafy ([`99273a8`](https://github.com/mps-youtube/yewtube/commit/99273a8e818ee8b69cdf69a9a74f72875e157f4c))

* Update version number ([`2b6ba3b`](https://github.com/mps-youtube/yewtube/commit/2b6ba3bfaa9ffc82347d9f7b2b83ed201db84e28))

## v0.2.2 (2015-02-14)

### Unknown

* Updated changes ([`3e684f9`](https://github.com/mps-youtube/yewtube/commit/3e684f9859b4bfb48f396771a25ed6561a61b099))

* Update version number ([`8aaf71f`](https://github.com/mps-youtube/yewtube/commit/8aaf71fcd66bbf76c38f7f88e5b38aca51c67caf))

* Update version number ([`3149b06`](https://github.com/mps-youtube/yewtube/commit/3149b061bff4fd539df027ca59662b8a1a87f901))

* Add release date ([`3f1f5f5`](https://github.com/mps-youtube/yewtube/commit/3f1f5f5397f91527fe0940f69eb5cae1e9165c0f))

* Update changes ([`5746e67`](https://github.com/mps-youtube/yewtube/commit/5746e67dcef683d3246abbe80dfba835ec1f99fa))

* Enable audio remux when using &#34;d&#34; command
previously it only worked with &#34;da&#34; command

This fixes issues with opening m4a audio files in iTunes and certain
other players. ([`5145267`](https://github.com/mps-youtube/yewtube/commit/5145267173aeb834df7a20e53c739fd019eb0938))

* Update changes ([`daed8bf`](https://github.com/mps-youtube/yewtube/commit/daed8bf6e2c3a2ce1c96e5b5301d3957a7da1db1))

* Remove file, to be added to separate branch ([`1351550`](https://github.com/mps-youtube/yewtube/commit/1351550426aed623d8bb942f25a0abb4ed338d9d))

* Add 2015 to copyright text
change nagev to np1 ([`9275a8c`](https://github.com/mps-youtube/yewtube/commit/9275a8c12162843306e82c87a187694042aaa0cd))

* remove newlines ([`72cf1d8`](https://github.com/mps-youtube/yewtube/commit/72cf1d82d54cf25e8117edfbbeae4180c29eabca))

* Document download_command option ([`838cc47`](https://github.com/mps-youtube/yewtube/commit/838cc477c6f23d248193ef4b234c9603df79b525))

* Improve download_command

%u will be replaced with the remote media content url
%d will be replaced with the download directory (as set by DDIR in mpsyt config)
%f will be replaced with the filename of the item being downloaded
%F will be replaced with the full file path (%d/%f)

for example, to download using aria2c:

`set download_command aria2c --dir=%d --out=%f %u`

Note that using a custom download command does not support transcoding the
downloaded file to another format with mps-youtube. ([`025bee5`](https://github.com/mps-youtube/yewtube/commit/025bee5351a03deb78c88f9990a063e1f79b7794))

* Update required pafy version ([`fb4ef3a`](https://github.com/mps-youtube/yewtube/commit/fb4ef3a518fb6cde113e92e9928ad4bfdad36a3f))

* require pafy 0.3.70 or later ([`7fb0b18`](https://github.com/mps-youtube/yewtube/commit/7fb0b1815932d2be21ed4fc8a1b360f5c345b8fd))

* Move input file code to separate function ([`a4092f4`](https://github.com/mps-youtube/yewtube/commit/a4092f4547bd185d07747e7bf75b4bc84374488e))

* tidy ([`d5744ad`](https://github.com/mps-youtube/yewtube/commit/d5744ad159fdd1591025dcc75300e94be1ef54ad))

* Update new features help topic ([`29cfb77`](https://github.com/mps-youtube/yewtube/commit/29cfb77e76888c2902ec6ee9c9d86b5cafc69ddc))

* Remove mpv/mplayer-input.conf config setting

Enable if file found in mpsyt config dir ([`8249068`](https://github.com/mps-youtube/yewtube/commit/82490681f9bdca3166fd3a822bb4fdb243df0670))

* Merge pull request #207 from ids1024/py2exesepratesetup.py

Use separate setup script for py2exe ([`2b308be`](https://github.com/mps-youtube/yewtube/commit/2b308bed9d74b1b0d9224d706b3f6303df1f51f6))

* Always import py2exe in setup_py2exe.py ([`5865954`](https://github.com/mps-youtube/yewtube/commit/5865954fcdc1ebc19b8e92aab84800d0082a631f))

* Use separate setup script for py2exe

The py2exe code in setup.py causes issues for pip ([`2e354d9`](https://github.com/mps-youtube/yewtube/commit/2e354d9f49386a6ca1d45f4edfa1ed57bab29d9c))

* Merge pull request #206 from ids1024/develop

Show &gt;/&lt; instead of n/p as keys for controlling player ([`c11ab87`](https://github.com/mps-youtube/yewtube/commit/c11ab87dd9131983261b7e3b1b02c14778e0cfe0))

* Show &gt;/&lt; instead of n/p as keys for controlling player ([`84d08f8`](https://github.com/mps-youtube/yewtube/commit/84d08f88bc0ba7048ffa5778303828ae722101e4))

* Merge pull request #198 from ids1024/develop

Add download_command option ([`0c1e45b`](https://github.com/mps-youtube/yewtube/commit/0c1e45bcd1107af7909c9c061e192f2c78804be2))

* Add download_command option

To make mpsyt use aria2c to download:
set download_command aria2c -d / -o &#39;%f&#39; &#39;%u&#39; ([`a1248a7`](https://github.com/mps-youtube/yewtube/commit/a1248a7b3cdcf4bc90be7043effddc6df84ea904))

* Use isinstace instead of type(variable) == Type ([`f1ec26c`](https://github.com/mps-youtube/yewtube/commit/f1ec26c8e79649521ecac7887b84b9dce6e3728d))

* Merge pull request #204 from ids1024/fix-racecondition

Fix race condition in mpv 0.7+ code ([`47964ce`](https://github.com/mps-youtube/yewtube/commit/47964ce766fa7c5ebd3d4d4210df1af8f6fe67ac))

* Move running test to while statement ([`cebc73e`](https://github.com/mps-youtube/yewtube/commit/cebc73e6df347634ddc3147f407a86533bc4ffd5))

* Actually increment tries variable; stop trying if process exited ([`81756af`](https://github.com/mps-youtube/yewtube/commit/81756afa4cefcb34725aa001573d15a0d164c428))

* Fix race condition in mpv 0.7+ code ([`85d5244`](https://github.com/mps-youtube/yewtube/commit/85d5244820c6164e83d278febd68d190ef605c09))

* Fix for FreeBSD (gh-199) ([`38a93b9`](https://github.com/mps-youtube/yewtube/commit/38a93b9cd13eb9cb2f7f7ad9077a6fb4f383b2b2))

* Merge pull request #203 from ids1024/terminalsize-fix

Make tuple_xy default to None rather than (None, None) ([`f1021ba`](https://github.com/mps-youtube/yewtube/commit/f1021baa246df96b91bf62aabe185493f0b07df2))

* Make tuple_xy default to None rather than (None, None)

This fixes the comparison of tuple_xy to None ([`fc80c80`](https://github.com/mps-youtube/yewtube/commit/fc80c807c92550c286c00b5cf13c306242f250e3))

* Merge pull request #195 from ids1024/develop

Use default useragent ([`5e82d43`](https://github.com/mps-youtube/yewtube/commit/5e82d43e00d4329aaa8657e6dfe2b5f46691d73c))

* Use default useragent ([`873411a`](https://github.com/mps-youtube/yewtube/commit/873411a691fb927da0f02356ff6efaaeb4617775))

* Merge branch &#39;develop&#39; into pr190

Conflicts:
	setup.py ([`f4b9a4d`](https://github.com/mps-youtube/yewtube/commit/f4b9a4d0fbb7ecb13431812c681cfa1ccad7d45d))

* Merge branch &#39;develop&#39; of https://github.com/np1/mps-youtube into develop ([`d86c05d`](https://github.com/mps-youtube/yewtube/commit/d86c05d57abe0c0b973c0a4a0d2028056ddae2bb))

* Merge pull request #194 from ids1024/develop

Minor code improvements ([`c685589`](https://github.com/mps-youtube/yewtube/commit/c6855899c5ad80e508b03160e25e9f3619bf642a))

* Fix incorrect getxy() call ([`59a89e4`](https://github.com/mps-youtube/yewtube/commit/59a89e42e4c3892039369726f415b5d7ee5ddce9))

* Make player_status() handle match_object instead of make_status_line()

make_status_line() should not have to know about the implementation of
the function calling it. ([`0d34937`](https://github.com/mps-youtube/yewtube/commit/0d349378a35de7812ed9cfbc23160cc64a5f4328))

* Do not store os.path.exists in temporary variable

Serves no purpose but to make the code more confusing ([`138fb60`](https://github.com/mps-youtube/yewtube/commit/138fb6000605dc41a6c8f27b0019cb7fbccebc14))

* Remove explicit type conversion

&#39;not value&#39; always returns a bool ([`492b205`](https://github.com/mps-youtube/yewtube/commit/492b205cd15e4a82235c13ea898452d3bbcea4db))

* Remove redundant test

os.path.isfile also tests that the file exists ([`908c2d2`](https://github.com/mps-youtube/yewtube/commit/908c2d2c57be560a7074ccd76d5af1acbca1e828))

* Make getxy return namedtuple ([`5ca5959`](https://github.com/mps-youtube/yewtube/commit/5ca59590ce4e87a17212dc8324cadbb9defa92d1))

* Merge pull request #188 from ids1024/develop

Add mpv_input_conf and mplayer_input_conf settings ([`3581973`](https://github.com/mps-youtube/yewtube/commit/3581973a955fa131cb63455b590e03e6b7ce3b0a))

* Remove try/except in launch_player finally statement

Also add tests to make the except statement unnecessary ([`fd20f74`](https://github.com/mps-youtube/yewtube/commit/fd20f748ea23fc65a74cda435618945f76a86146))

* Fix bug in socket deleting

Sockpath was not defined for mplayer, causing an error, which went
unnoticed due to the except statement. ([`2639dd9`](https://github.com/mps-youtube/yewtube/commit/2639dd94433b1793952a94e6ba0888c4c94110d8))

* Fix returncode handling logic for finishing song ([`37d66fb`](https://github.com/mps-youtube/yewtube/commit/37d66fbbe11e653c0917a096af2ff37950d61d41))

* Fix returncode handling logic and do not redefine builtin &#39;file&#39; ([`d51475c`](https://github.com/mps-youtube/yewtube/commit/d51475c1af651a25e175a51b5b2f5e1506cad8e7))

* Add mpv_input_conf and mplayer_input_conf settings

Allow setting an input.conf to override defaults.  Also makes the
default keys for next/prev the same as the mpv/mplayer defaults. ([`e1b24a1`](https://github.com/mps-youtube/yewtube/commit/e1b24a1a694890cae569cfb2bcfb8080f060763d))

* Update pafy version ([`2701f2b`](https://github.com/mps-youtube/yewtube/commit/2701f2bd8ef654b4f8b5fb5fe06d127d130bbf25))

* Make py2exe build binary not require additional dlls ([`846fbc1`](https://github.com/mps-youtube/yewtube/commit/846fbc1143fceb69b86586fd19c585d5df659603))

* Support py2exe ([`5caca6b`](https://github.com/mps-youtube/yewtube/commit/5caca6b8df91b5a7a99d597c8663c100cc2632af))

* Merge branch &#39;master&#39; into develop ([`c988503`](https://github.com/mps-youtube/yewtube/commit/c988503ae273b0058fb5d509f73e97bc20d0a91f))

* Update install notes ([`e2feb71`](https://github.com/mps-youtube/yewtube/commit/e2feb713cef3b5acf55dda97e87a39ec3ff18c5c))

* Fix format string arguments ([`595e1ce`](https://github.com/mps-youtube/yewtube/commit/595e1cee7df7653e3f119d25c1adec6c5ae0e53f))

* Add pylint ignores ([`080764f`](https://github.com/mps-youtube/yewtube/commit/080764f076d6cf99ff50d421890ab56d949476b9))

* tidyup ([`9cb2e3f`](https://github.com/mps-youtube/yewtube/commit/9cb2e3fcbe4545b0072b65858584e44c85b888ee))

* Add code health badge ([`d6c212a`](https://github.com/mps-youtube/yewtube/commit/d6c212a779314881b3e2550bb39be4123a25c539))

* Add version notes to debug output ([`cde7b69`](https://github.com/mps-youtube/yewtube/commit/cde7b6962c99c3d02bade78892a500df97ff28e6))

* remove __main__.* assignments ([`84e3fec`](https://github.com/mps-youtube/yewtube/commit/84e3fec61a8c2f768d48e6eacc4708ad4d9617e0))

* Remove redundant lines in launch_player() ([`0196394`](https://github.com/mps-youtube/yewtube/commit/01963942fd97125dbdcdb6d40e5267cf20785c6d))

* Spacing and PEP8 ([`6b0620c`](https://github.com/mps-youtube/yewtube/commit/6b0620cafc908044f39f1f637b93dfee1f22032d))

* Merge pull request #181 from ids1024/exenamealways

Always pass exename to get_mpv_version ([`9b980c5`](https://github.com/mps-youtube/yewtube/commit/9b980c50aac5492f1c441557b0be9421868a9db8))

* Improve player name recognition ([`94f4f4d`](https://github.com/mps-youtube/yewtube/commit/94f4f4dbfc54775061ecf0d23b06c3c1aba818c9))

* Always pass exename to get_mpv_version ([`d1a2633`](https://github.com/mps-youtube/yewtube/commit/d1a263335ae2017ea8ecc79e945eb360df96c9af))

* Merge pull request #184 from ids1024/exitcodesuccess

Use return code to determine if player succeeded ([`6a27d83`](https://github.com/mps-youtube/yewtube/commit/6a27d8391d43dff571a13d7c321ab8b29266cd7a))

* Fix returncode handling on OSError ([`ffddb74`](https://github.com/mps-youtube/yewtube/commit/ffddb74dc00162fabd048b68a6244deefaaf487a))

* Use return code to determine if player succeeded ([`e2f9cb7`](https://github.com/mps-youtube/yewtube/commit/e2f9cb71965ec8fe7197ea9773dacb992d187ce6))

* Merge pull request #187 from ids1024/develop

Dead code removal / Minor bug fixes / Minor improvement ([`9c0d05b`](https://github.com/mps-youtube/yewtube/commit/9c0d05b026bfc56006d9835ba4f0aa61c46aedbe))

* Do not attempt to run .split() on a list ([`dc5581e`](https://github.com/mps-youtube/yewtube/commit/dc5581e1bac418b25e3bc761e582f3415bec8b2b))

* Store command regex mappings by function rather than function name ([`7a6fe4f`](https://github.com/mps-youtube/yewtube/commit/7a6fe4f67cd08f762c3df0e3eb8c33f7ea123e6b))

* Remove top command

Command from mps that does not exist in mps-youtube ([`684bb77`](https://github.com/mps-youtube/yewtube/commit/684bb77ff8ed005b24d5d1941550110b503f5ce7))

* Remove dead/redundant code ([`59e6d3a`](https://github.com/mps-youtube/yewtube/commit/59e6d3a6a6dbe60661211e9c0ab5b51313fd70c5))

* Merge pull request #185 from ids1024/openhyphen

Replace spaces with hyphens in &#39;open&#39; and &#39;view&#39; commands ([`0a7870e`](https://github.com/mps-youtube/yewtube/commit/0a7870e9ae9f05e518747ea1bbb82e179fc9d58e))

* Replace spaces with hyphens in &#39;open&#39; and &#39;view&#39; commands ([`230cebd`](https://github.com/mps-youtube/yewtube/commit/230cebd197cb1a50ffdf5fca23364fdbb7a38cbe))

* Merge pull request #183 from ids1024/issue156

Override quiet option in mplayer ([`46e5064`](https://github.com/mps-youtube/yewtube/commit/46e50648c67248343771187acef6647f1a70352d))

* Override quiet option in mplayer

In the default config on Windows, interferes with reading status. ([`98f18d1`](https://github.com/mps-youtube/yewtube/commit/98f18d1cbfccdb300ae6c1513c2c7c41d9bee4c7))

* Merge pull request #180 from ids1024/develop

Fix input_file for mplayer on Windows ([`e51d47f`](https://github.com/mps-youtube/yewtube/commit/e51d47ffac35d6c03d7d064189903416be8b7a7e))

* Replace \ with / in input path with Windows mplayer ([`11b16e2`](https://github.com/mps-youtube/yewtube/commit/11b16e26fe8539c8dd1a2bb8dc5b1199cbbe14e7))

* Fix input_file for mplayer on Windows ([`8d8aab5`](https://github.com/mps-youtube/yewtube/commit/8d8aab54782492e9c0f043ca7a757f5b7ed9641c))

* Merge pull request #176 from ids1024/develop

Display volume when using mpv 0.7+ with json IPC ([`55681b9`](https://github.com/mps-youtube/yewtube/commit/55681b9174bcb2471c8c38959fabfd46d8b61373))

* Display volume when using mpv 0.7+ with json IPC ([`1e18865`](https://github.com/mps-youtube/yewtube/commit/1e188658214feaec0e6b478c2af35c5f06b36b56))

* Hide mpv error messages in mpv v0.7+ ([`bdac88b`](https://github.com/mps-youtube/yewtube/commit/bdac88bc9e5e94f2837050811f05fc46f1f41a89))

* Don&#39;t quit when p is pressed on first item ([`1b74a5f`](https://github.com/mps-youtube/yewtube/commit/1b74a5fa5df52b35935ab468f0df2e6b06573f63))

* Updated changes ([`da79ca2`](https://github.com/mps-youtube/yewtube/commit/da79ca2e21b447a6f58826deb407c0302973c4e5))

* Merge branch &#39;prev-track&#39; into develop ([`bf5c268`](https://github.com/mps-youtube/yewtube/commit/bf5c268dc498b1c66a501c5bc9654a15af8cba10))

* Use n/p for next/prev (#175)
update player key help
also allow j/k for next/prev
Use q to quit playing through a list instead of ctrl-c

The p key conflicts with pause, shouldn&#39;t be a problem as spacebar can be
used ([`6c60f50`](https://github.com/mps-youtube/yewtube/commit/6c60f508f46d242f324ec7ae52fb3aa99dd95b8e))

* Fix invalid syntax for Python 2.7 ([`73f67a4`](https://github.com/mps-youtube/yewtube/commit/73f67a41ea087fd797e6cd1bc7dc3596ee2ffd32))

* Merge remote-tracking branch &#39;origin/pr/175&#39; into prev-track

Conflicts:
	mps_youtube/main.py ([`5ff107d`](https://github.com/mps-youtube/yewtube/commit/5ff107d5b2d27d65f7a3b241ecf8df45fa986212))

* Catch socket.error in mpv socket code

Before the message &#34;mpv was not found on this system&#34; showed up
sometimes, apparently when mpv was quit too quickly, before mpsyt could
connect to the socket. This removes the incorrect error message. ([`793c1f1`](https://github.com/mps-youtube/yewtube/commit/793c1f15acf88cb3e01fd967542bb95ad4322fcf))

* Combine nested while loops into one loop ([`48cf0b9`](https://github.com/mps-youtube/yewtube/commit/48cf0b98d04e477d790dd3bf2a9c2342c643d9ee))

* Unlink temporary files before trying to terminate player ([`ed603b3`](https://github.com/mps-youtube/yewtube/commit/ed603b3fdde8ecab3348ba2e5b197d39572ece00))

* Fix going backwards in playlist with mplayer ([`520e4ec`](https://github.com/mps-youtube/yewtube/commit/520e4eca078f50d86fce3f13b987aee3c1149319))

* Go to last track when going backwards from first track ([`8af673f`](https://github.com/mps-youtube/yewtube/commit/8af673f3269a4822c4f1b7d49019f426ec2064d1))

* Allow going backwards in playlist ([`4386c32`](https://github.com/mps-youtube/yewtube/commit/4386c32ee81c2d861de5eb9a9b3f1c66d5b89e7b))

* Remove redundant code ([`a831549`](https://github.com/mps-youtube/yewtube/commit/a831549249bfee4788cfae3fd7b16e401884ecc5))

* Add pylint ignore ([`c9607db`](https://github.com/mps-youtube/yewtube/commit/c9607db36da40a3851619b0c991c52509e65f824))

* Updated changes ([`5a5c71b`](https://github.com/mps-youtube/yewtube/commit/5a5c71b697a806b4773612c3fc334a0a206a549c))

* Move checking of mpv unix socket support
(don&#39;t check each time an item is played) ([`c9757b4`](https://github.com/mps-youtube/yewtube/commit/c9757b444c03fb7c00a89d8277404575fa90c58f))

* PEP8 fixes ([`241f183`](https://github.com/mps-youtube/yewtube/commit/241f183a665556911ed91775c2c3d848021361b4))

* Merge remote-tracking branch &#39;origin/pr/161&#39; into mpv0.7fix2 ([`f548312`](https://github.com/mps-youtube/yewtube/commit/f548312621d031b7d407b743d5e16e4a125e1e21))

* Catch socket.error in mpv socket code

Before the message &#34;mpv was not found on this system&#34; showed up
sometimes, apparently when mpv was quit too quickly, before mpsyt could
connect to the socket. This removes the incorrect error message. ([`649a167`](https://github.com/mps-youtube/yewtube/commit/649a167e7d25346a0cacab149db9eb7a47f3a9f7))

* Use --list-options to determine if mpv supports --input-unix-socket ([`30f790a`](https://github.com/mps-youtube/yewtube/commit/30f790a134062d4fba47c3674f669b2209895d54))

* Merge remote-tracking branch &#39;np1/develop&#39; into develop ([`ed237ee`](https://github.com/mps-youtube/yewtube/commit/ed237ee6c6111b722737f92722097f5d75ab542f))

* Use random socket name and unlink after use ([`7b06f71`](https://github.com/mps-youtube/yewtube/commit/7b06f71f9a76f75acca1aa84fd85eba24356202e))

* Iterate over lines in socket properly

The other method was a hack ([`8a0a06a`](https://github.com/mps-youtube/yewtube/commit/8a0a06a11ebc213d7551da733bc3a07b39da946f))

* Keep lines down to 80 characters ([`70832ff`](https://github.com/mps-youtube/yewtube/commit/70832ff25fb931554a0988a4beac17c6c9aa9750))

* Use Json IPC for mpv 0.7+ on unix ([`f7fb052`](https://github.com/mps-youtube/yewtube/commit/f7fb0526e8ea26f906c47ba7ddf80a767ec84609))

* Merge branch &#39;develop&#39; of https://github.com/np1/mps-youtube into develop ([`9b8d839`](https://github.com/mps-youtube/yewtube/commit/9b8d8399836b808dfc0505b62e0ea06da113ad2c))

* Merge pull request #167 from bradleyjkemp/develop

Created unit tests for fmt_time() and num_repr() ([`2a7a39a`](https://github.com/mps-youtube/yewtube/commit/2a7a39a5d66fb6becf6b2c080a862ed8f64d6991))

* Corrected an incorrect test.
If time is less than 1:40:00 then we display it in minutes only. ([`72e1991`](https://github.com/mps-youtube/yewtube/commit/72e199133366fa4b195b14bddf79901172190271))

* Created the test directory. Added the first unit test. Removed test* from .gitignore ([`d220440`](https://github.com/mps-youtube/yewtube/commit/d220440ddf2cebdd838c8f7c7c5f510571e9b1e4))

* Documented changes ([`4c51a15`](https://github.com/mps-youtube/yewtube/commit/4c51a15c9bb7d7db0ef6aeb3abf8ccee79cb84a1))

* Keep status line length uniform (#163)
remove streams listing from video info screen ([`473e6bc`](https://github.com/mps-youtube/yewtube/commit/473e6bc8d50cb1904c104064f543199a89e0a98d))

* Merge branch &#39;develop&#39; into HEAD ([`ffe77f2`](https://github.com/mps-youtube/yewtube/commit/ffe77f20a54bd0067c3cb538d75cafa2ad97da73))

* Fix YT comments overshoot window size ([`9812c8b`](https://github.com/mps-youtube/yewtube/commit/9812c8b9c3f64ed12419ad92ded4de5ef92dbc3b))

## v0.2.1 (2014-11-27)

### Unknown

* Update changelog ([`c410849`](https://github.com/mps-youtube/yewtube/commit/c410849039573cc646a6303e6f3e93014e9e78a5))

* Bump version to 0.2.1 ([`f44f525`](https://github.com/mps-youtube/yewtube/commit/f44f52532752a32da057358c1b839e333cd2f145))

* Merge branch &#39;xprint&#39; into develop ([`c878bb2`](https://github.com/mps-youtube/yewtube/commit/c878bb2203f010da4c93ea6f3dfc13f88c3a0534))

* use xprint more ([`aa0edc0`](https://github.com/mps-youtube/yewtube/commit/aa0edc01670d5682924887e8086818bd4325ad58))

* Don&#39;t attempt to play with invalid player setting ([`d886bf7`](https://github.com/mps-youtube/yewtube/commit/d886bf7f2f8d3044b56e4976b1290bdbb34ef678))

* Add .exe to Windows player check function ([`f7b3907`](https://github.com/mps-youtube/yewtube/commit/f7b3907353fc3e135a909b8722033040a1893268))

* Fix setting default player ([`1e9eccd`](https://github.com/mps-youtube/yewtube/commit/1e9eccd2a58858c78ee0cee12a6f88987fd1d5ec))

* Set player for new installs (#149) ([`56f9237`](https://github.com/mps-youtube/yewtube/commit/56f9237adab5f39433b0414dc345a737086c01ae))

* Update display commands ([`6f7a7ea`](https://github.com/mps-youtube/yewtube/commit/6f7a7ea6cb2c9e532d0f8417af8e4f9789e8e95f))

* Update description ([`c36f015`](https://github.com/mps-youtube/yewtube/commit/c36f015fe2a10154893e977665e7b5d1b1f92bd0))

## v0.2.0 (2014-11-25)

### Unknown

* Add release date ([`c10dba9`](https://github.com/mps-youtube/yewtube/commit/c10dba918691b3360252cf316504353c78076ef2))

* fix update msg ([`cf17422`](https://github.com/mps-youtube/yewtube/commit/cf17422b3b20fea77650cdf6aa3a76dcf5dcc08b))

* Merge branch &#39;hasb&#39; into develop ([`e3fa5b9`](https://github.com/mps-youtube/yewtube/commit/e3fa5b9f557fa393c1cefa8c623609e73c302dd4))

* bump version number ([`4d4e541`](https://github.com/mps-youtube/yewtube/commit/4d4e541025ecc91be25c0aca3c2f8c7a470179fb))

* tidy logo ([`18a40f0`](https://github.com/mps-youtube/yewtube/commit/18a40f0a841da4156c6da0ad6754b1ba7c335775))

* logo alignment ([`13701cd`](https://github.com/mps-youtube/yewtube/commit/13701cdbaeccdf8c2d47d43fc4ae3b9499a53536))

* fix mplayer m4a handling in windows ([`cf031f1`](https://github.com/mps-youtube/yewtube/commit/cf031f1237343540c5daf2831d0879616934a778))

* Fix windows player filename issue ([`9753ea0`](https://github.com/mps-youtube/yewtube/commit/9753ea093609edf65c0e4280cdc094aa5310b1b2))

* Enable detect terminal size by default for all platforms ([`6945d6f`](https://github.com/mps-youtube/yewtube/commit/6945d6f3a0bcb052f42532657db889dc66b7b4e0))

* Windows compatibility fixes ([`67e9cf0`](https://github.com/mps-youtube/yewtube/commit/67e9cf0b02c0ea6bd8275ee939f77759464a6769))

* tidy logo ([`2d26e32`](https://github.com/mps-youtube/yewtube/commit/2d26e320924a779f5a6a9bc642c2bc91db8f8685))

* Display volume changes in audio mode ([`e3bac87`](https://github.com/mps-youtube/yewtube/commit/e3bac87a03f34848e8b98177556dc36003bd637e))

* Fix number alignment in result list and encoder selection ([`78a47c5`](https://github.com/mps-youtube/yewtube/commit/78a47c52c0cf868e7564c5a49a44689cf14ed296))

* Don&#39;t transcode audio when muxing ([`98ea3dc`](https://github.com/mps-youtube/yewtube/commit/98ea3dc104bd664fb918a524a10e175c7fad211c))

* fix splitting filename components ([`ce4b82e`](https://github.com/mps-youtube/yewtube/commit/ce4b82e8730b3e45a9262916a0fb26f76bf3e4c3))

* fix playback display alignment ([`c0994fd`](https://github.com/mps-youtube/yewtube/commit/c0994fddf7eb34eeb608b51f3508735b28aefb70))

* require latest pafy (0.3.66) ([`5a315d6`](https://github.com/mps-youtube/yewtube/commit/5a315d67a94f9e3f90a7119dc588ddbf0cad8f33))

* Fixed bug where progress bar would be split over two lines ([`0fd59d3`](https://github.com/mps-youtube/yewtube/commit/0fd59d387450b7a03d33ff21afb3cf2b8bd0101f))

* Additional information displayed ([`79c1532`](https://github.com/mps-youtube/yewtube/commit/79c1532f9ec615c7b8d4daf6b5ffba7e5b44fcb4))

* PEP8 changes ([`e15c88c`](https://github.com/mps-youtube/yewtube/commit/e15c88c60430f439891b20fdd02505b2741c91cd))

* Updated changes ([`fb36dea`](https://github.com/mps-youtube/yewtube/commit/fb36deaf42f49d9e62c4dc559f17100cb93e55c1))

* Detailed new features for help topic ([`71c3715`](https://github.com/mps-youtube/yewtube/commit/71c3715d5e7aa63932855bfa583e2af24d5b8c39))

* Fix download queue heading ([`353cf88`](https://github.com/mps-youtube/yewtube/commit/353cf88a6e7b263e1187d65a780eec492d062bd2))

* Fix encoding preset init, tidy display ([`11f812e`](https://github.com/mps-youtube/yewtube/commit/11f812e18ce7b9a4ac6e2bbe422f23780202f46a))

* Add timeout for update check ([`c41b4d0`](https://github.com/mps-youtube/yewtube/commit/c41b4d0fd68de7c91c6807c50c5e0839e158a9f8))

* refresh ascii logo, centre in terminal window ([`6bfff60`](https://github.com/mps-youtube/yewtube/commit/6bfff60436db756139776b0d53b1962691e4fe38))

* Merge branch &#39;transcoding&#39; into develop ([`f67254b`](https://github.com/mps-youtube/yewtube/commit/f67254b5850ecb347d5d388ca911d52dadbcccf7))

* Implement transcoding of downloaded files ([`c66e9ce`](https://github.com/mps-youtube/yewtube/commit/c66e9cec06f026bb6346c4e1642aab9193e46052))

* Remove signature argument to pafy.new (#147) ([`c5cc455`](https://github.com/mps-youtube/yewtube/commit/c5cc455fdf65f074b54095bd9c89db1acf18b2a3))

* documented changes ([`c11ed0f`](https://github.com/mps-youtube/yewtube/commit/c11ed0f895271746d32a758f62bbe8a232cf0b6e))

* remove debug print ([`43957cb`](https://github.com/mps-youtube/yewtube/commit/43957cbce27bb3cce492a531a6da08e0c6a48155))

* Remux audio files for better compatibility (#135) ([`32e9739`](https://github.com/mps-youtube/yewtube/commit/32e9739f0a0b65f47d1e7f8ca536fa9a3e5feb93))

* Updated changes ([`59c6cdf`](https://github.com/mps-youtube/yewtube/commit/59c6cdf17b2213cfef5cee6d555ce67140cb55e8))

* remove previous merge code duplication ([`031c903`](https://github.com/mps-youtube/yewtube/commit/031c9036d3257dacf4ec21ee6558499da154cce4))

* auto detect terminal size by default on linux and mac ([`2fd38bf`](https://github.com/mps-youtube/yewtube/commit/2fd38bfa7995be0a0f8522c643372272153241e3))

* Merge branch &#39;develop&#39; into autodetect-terminal-size

Conflicts:
	mps_youtube/main.py ([`4d2089d`](https://github.com/mps-youtube/yewtube/commit/4d2089d7095c79676af52df43725898b961f6e97))

* move help text ([`cf1aada`](https://github.com/mps-youtube/yewtube/commit/cf1aadaec32fdd6a20fc1ee151d556699728c504))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`77329d5`](https://github.com/mps-youtube/yewtube/commit/77329d5cf471cddcb008944f122b67ccee739b6a))

* move import statement ([`b1145f0`](https://github.com/mps-youtube/yewtube/commit/b1145f0715243e7808c33670b530d75a1a0a2037))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`9523b04`](https://github.com/mps-youtube/yewtube/commit/9523b0444ed377376abf15d27f42190a0f17f7e6))

* Added troubleshooting link ([`e8ad6eb`](https://github.com/mps-youtube/yewtube/commit/e8ad6eb477c69544c51b0e868f05ae806ef5b74e))

* Updated changes ([`4762909`](https://github.com/mps-youtube/yewtube/commit/4762909121fd55332f28a1e6b24956b8481c3405))

* Fix setting expanded ddir (#136) ([`a854345`](https://github.com/mps-youtube/yewtube/commit/a854345c65779b875430cccda7108400cccb3027))

* Merge pull request #136 from punchagan/set-ddir-expanduser

Allow setting ddir using ~/path/ ([`41b683e`](https://github.com/mps-youtube/yewtube/commit/41b683e55a3918a0e3ebca4837f92645e87f03d7))

* Allow setting ddir using ~/path/ ([`6edd5b5`](https://github.com/mps-youtube/yewtube/commit/6edd5b56e4dd9d44c34398c54e82fe8ab19ff993))

* Merge pull request #131 from vitorgalvao/patch-1

README: how to install mplayer with homebrew ([`c38d2ed`](https://github.com/mps-youtube/yewtube/commit/c38d2ed6c31d8b475ad5157f0f8dfd3d80dc9d3d))

* README: how to install mplayer with homebrew

Applies to OS X instructions. ([`5073ac6`](https://github.com/mps-youtube/yewtube/commit/5073ac6441475c232a7a2c7cf9d12e3ed88ff15a))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`82cff62`](https://github.com/mps-youtube/yewtube/commit/82cff62952795c87db143ef387da7a6ea6251fa8))

* Merge pull request #125 from YoussF/develop

Temporary downloaded file name bug fix (Bug report #122) ([`ca16fa8`](https://github.com/mps-youtube/yewtube/commit/ca16fa8aa068db80ba179f53a34b0067e752ce96))

* Temporary downloaded file name bug fix (Bug report #122) ([`56ba134`](https://github.com/mps-youtube/yewtube/commit/56ba1349637302d6a60342c04a794a4a8806ddea))

* Fix mux ([`f4a903d`](https://github.com/mps-youtube/yewtube/commit/f4a903d2075d3cc7c79c71dd4d9e58b1cfc17402))

* Fix rst formatting ([`49cea8a`](https://github.com/mps-youtube/yewtube/commit/49cea8ab9b4f9f5b60cb13141e8f60c59cd79aa1))

* Update Windows install notes (#116) ([`7bd4986`](https://github.com/mps-youtube/yewtube/commit/7bd4986ac5c584bf9985a9661db17842619ee580))

* Merge branch &#39;develop&#39; into autodetect-terminal-size

Conflicts:
	mps_youtube/main.py ([`57a298a`](https://github.com/mps-youtube/yewtube/commit/57a298ac627d4370b8dc60bac141078e98b37848))

* add --no-preload option ([`8f14d7b`](https://github.com/mps-youtube/yewtube/commit/8f14d7b915d8c72d1480f36947aa0bc7a6cde186))

* tidy help text ([`26b7e6d`](https://github.com/mps-youtube/yewtube/commit/26b7e6d9cc68d22e7b5fd593cc83a47578e7d03f))

* Merge pull request #114 from mtahmed/mtahmed-develop

Add the ability to download all the playlists by a user. ([`b075abc`](https://github.com/mps-youtube/yewtube/commit/b075abc2cf6536f31dab2283a35bb553a92c034f))

* Add the ability to download all the playlists by a user.

The daupl and dvupl commands allow the user to download the audio or the
video for all the tracks in all the playlists for a user respectively. ([`2be9b89`](https://github.com/mps-youtube/yewtube/commit/2be9b89e62a5e814c956946a801cc9a31f23de0d))

* Updated changes ([`b8aaa7e`](https://github.com/mps-youtube/yewtube/commit/b8aaa7ee9195b9b135798e1dab7663656125af74))

* Enable da and dv command for playlist results ([`c7648bd`](https://github.com/mps-youtube/yewtube/commit/c7648bdaa6d1139287fbb9ee4ac6ab25781a1e95))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`b0eccc0`](https://github.com/mps-youtube/yewtube/commit/b0eccc0bce19ed8330448a0fcd994fa782180391))

* Merge branch &#39;pr/110&#39; into develop ([`1b348f3`](https://github.com/mps-youtube/yewtube/commit/1b348f37a48e71593fd97ea2f20e8c2a5c8fd4d2))

* Remove repeated code (#110)

Replace invalid characters in subdirectory name ([`04fb863`](https://github.com/mps-youtube/yewtube/commit/04fb863fda35fa537ed1dea10c58b56cd1359d54))

* Add the ability to download a youtube playlist.

The dapl and dvpl commands take playlist URL or ID as paramters and
download all the audio or video tracks in the playlist respectively. It
creates a subdirectory in the default download directory named the same
as the playlist name. It then downloads all the tracks into the
subdirectory. ([`ad2a70a`](https://github.com/mps-youtube/yewtube/commit/ad2a70a36ce7b11e419502261ae639fbf0d2e051))

* Update changes ([`fca49a6`](https://github.com/mps-youtube/yewtube/commit/fca49a6d648ecc63b55e1bccfe94fd434ffe08cb))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`7c50808`](https://github.com/mps-youtube/yewtube/commit/7c50808bf454a4aa3a115c40195487246daa7ec2))

* Fix mpv msglevel argument #38 ([`a573fd6`](https://github.com/mps-youtube/yewtube/commit/a573fd6433677251bbc95dd0b8e84404be1dc79b))

* Fix for non-stable mpv version number #38 ([`10d936c`](https://github.com/mps-youtube/yewtube/commit/10d936c5f7d48f646fefb9f46cde8c54e57829d1))

* check mpv version for msglevel flag (#38) ([`71191ec`](https://github.com/mps-youtube/yewtube/commit/71191ec73de4ebb9c947bdc0ed9b42d943a0240e))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`cc11df9`](https://github.com/mps-youtube/yewtube/commit/cc11df97ae3b16697206ba005d6dee18a9376ca4))

* Display playing progress with mpv #38 ([`140260b`](https://github.com/mps-youtube/yewtube/commit/140260ba67003380c612bbd83dc32438dd977f4b))

* Don&#39;t use time to detect whether an item failed (#109) ([`3562709`](https://github.com/mps-youtube/yewtube/commit/3562709106012fbe81da7fa66e3fc3bf7dd5e4fa))

* Fix output with non tty stdout (#108) ([`36af308`](https://github.com/mps-youtube/yewtube/commit/36af308d54622a726dd8ccecd5a8b91dd1653f8c))

* output encoding info with --version ([`d7a4364`](https://github.com/mps-youtube/yewtube/commit/d7a43643c0da36300d9434f08238179c5e330af0))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`df5f200`](https://github.com/mps-youtube/yewtube/commit/df5f20040a36d029358e2140b275b985ebcb8663))

* Specify required pafy version (#104) ([`b0f73a4`](https://github.com/mps-youtube/yewtube/commit/b0f73a4bd9f5331644818efa55f881f7ddf1ab29))

* Revert &#34;Remove parameters to workaround broken gdata v2 api (gh-106)&#34;

This reverts commit 17516867b5b5ee81a159ef4e7d728fe36461096c. ([`b11e2dc`](https://github.com/mps-youtube/yewtube/commit/b11e2dcb53f68111cbf1147b192c357e65f7bfd6))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`b4ee8f0`](https://github.com/mps-youtube/yewtube/commit/b4ee8f005472ad90794cc688933cb7690f9f0d68))

* Remove parameters to workaround broken gdata v2 api (gh-106) ([`1751686`](https://github.com/mps-youtube/yewtube/commit/17516867b5b5ee81a159ef4e7d728fe36461096c))

* Updated new features topic ([`752dca3`](https://github.com/mps-youtube/yewtube/commit/752dca3d52638298b148f2ac3ac5301e8a3d77ec))

* Added ignore file ([`335ed3c`](https://github.com/mps-youtube/yewtube/commit/335ed3c39e4657a111911fe666729fbfc1ba3017))

* clear search result cache (#99) ([`a33563e`](https://github.com/mps-youtube/yewtube/commit/a33563eb33bf8440067c0c15f09734caff72fa7d))

* Accept two-character username (#99) ([`3f31a77`](https://github.com/mps-youtube/yewtube/commit/3f31a77025e360feea2c60a5ecea94abffd14f19))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`b76db95`](https://github.com/mps-youtube/yewtube/commit/b76db959b163d742cca47986435c00cb2cc4028b))

* Added clipboard copy feature (request #97) ([`59d331b`](https://github.com/mps-youtube/yewtube/commit/59d331b93a3e65c1a0d18e89e6a5feaae76687ca))

* Exit with correct status code ([`44ad87d`](https://github.com/mps-youtube/yewtube/commit/44ad87db4ce7f0c401947246b0276c5cfb0b5171))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`660aa9a`](https://github.com/mps-youtube/yewtube/commit/660aa9a15708748c061d028550692261d96b036f))

* remove unnecessary print ([`76dce84`](https://github.com/mps-youtube/yewtube/commit/76dce84614c806c84d00f8ba2eda9def4029b8de))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`73d7a1c`](https://github.com/mps-youtube/yewtube/commit/73d7a1c4097ed7cdd369014919e2e58b8f66a5a4))

* fix notify command doesn&#39;t work with &#39; char ([`a54074e`](https://github.com/mps-youtube/yewtube/commit/a54074e65455fc25e1a7124f91748a6ecbab40b6))

* Merge remote-tracking branch &#39;origin/pr/95&#39; into develop-pr95 ([`7acde93`](https://github.com/mps-youtube/yewtube/commit/7acde93dc7c54b2bfd521d4eb5f3a5a00d463d48))

* fix notifier bug with shell=True ([`bdd93c2`](https://github.com/mps-youtube/yewtube/commit/bdd93c24b684f9e39a3f50808c72ec721d738f12))

* use subprocess.call for notifier, don&#39;t depend on mplayer ([`8cec8ea`](https://github.com/mps-youtube/yewtube/commit/8cec8ea1ca37bdc7067fb726f340be54a6d0e365))

* removing unnecessary import ([`152109e`](https://github.com/mps-youtube/yewtube/commit/152109e30f9863e1ca2bddeb3e8bfe3410b38dd1))

* adding support for notifiers ([`20b0183`](https://github.com/mps-youtube/yewtube/commit/20b018357f7b9c142cca185e82d6688c7cb158d3))

* Fix order of help set topics ([`ca56e1f`](https://github.com/mps-youtube/yewtube/commit/ca56e1f2e99d08424bdb1cdc4c86800295d894ae))

* Merge remote-tracking branch &#39;origin/pr/93&#39; into develop ([`349a9e9`](https://github.com/mps-youtube/yewtube/commit/349a9e912c1bdea0617ac7373538154da37fcb77))

* Add the overwrite true|false option.

This option, if set to true, will overwrite existing downloaded files
but if set to false, will skip downloads for which there are existing
files in the current download directory. This allows for quickly
downloading new files in a playlist while ignoring the ones that are
already downloaded. ([`109fb66`](https://github.com/mps-youtube/yewtube/commit/109fb668339dc827837499be6a171cf7c9ea0dfd))

* Use smaller image link ([`4527918`](https://github.com/mps-youtube/yewtube/commit/452791822160c0ce113c70b0d681f4b1d746c512))

* Added branch to contrib notes ([`0e0a951`](https://github.com/mps-youtube/yewtube/commit/0e0a951060112a0f84e68518eebfc5441f63c60d))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`b5a11d0`](https://github.com/mps-youtube/yewtube/commit/b5a11d0ec5a06acbcd10dfdaf5695aa64bcb2fb0))

* fix encoding issue ([`69066d4`](https://github.com/mps-youtube/yewtube/commit/69066d419f651a062f7ec48f4fa69b3c48e009bf))

* Merge branch &#39;develop&#39; into autodetect-terminal-size

Conflicts:
	mps_youtube/main.py ([`c18d35d`](https://github.com/mps-youtube/yewtube/commit/c18d35d79a1062c23b19cac35713d1956cd13669))

* PEP cleanup ([`63a017d`](https://github.com/mps-youtube/yewtube/commit/63a017d83f5e3c3f8c26c6c282419bfb18a092ed))

* fix plist function for autosize ([`6912b52`](https://github.com/mps-youtube/yewtube/commit/6912b52e8972094dc91eb82aa812022e9756e2d6))

* Merge branch &#39;develop&#39; into autodetect-terminal-size ([`247678a`](https://github.com/mps-youtube/yewtube/commit/247678a7f3345bd34e8347d79421dde26ed262c7))

* log unrecognised config items ([`5c167c6`](https://github.com/mps-youtube/yewtube/commit/5c167c6cb4a1daa15dbc43e730371269456cff3e))

* Fix add many to playlist saves file repeatedly ([`7ac8120`](https://github.com/mps-youtube/yewtube/commit/7ac8120454af3285f825291d54cbf0bcec892b1d))

* Ignore unrecognised data in old configs

This handles the case of using a config file from a different version of mpsyt. ([`04d272c`](https://github.com/mps-youtube/yewtube/commit/04d272cc637f4bbcf3500bd88cd1e90c74adb53c))

* Added parameter to getxy function ([`c3604a7`](https://github.com/mps-youtube/yewtube/commit/c3604a75f1866aec7de191999d7ed04bf697404e))

* Remove messy underscore variables

Not sure why I was doing it that way instead of accessing result by index! ([`b1e97be`](https://github.com/mps-youtube/yewtube/commit/b1e97be11295f9cef567b818b2ce1ab3b7e5f511))

* Merge pull request #83 from thomasleveil/autodetect-terminal-size

fix --autosize not working when --debug or --logging is in use ([`4360ba1`](https://github.com/mps-youtube/yewtube/commit/4360ba1db90a7745ab156bf09346941b38198315))

* fix --autosize not working when --debug or --logging is in use ([`5894c68`](https://github.com/mps-youtube/yewtube/commit/5894c6888ca49d193eaa236b6b06204d66b775f1))

* Added terminal size detection ([`eb5f146`](https://github.com/mps-youtube/yewtube/commit/eb5f14615cdf8b922a270d33259d09d9e64a7944))

* added terminalsize module ([`f852b8d`](https://github.com/mps-youtube/yewtube/commit/f852b8d9bf3adde01fb2467e438a3c4b160e51a0))

* Use smaller image link ([`c68387e`](https://github.com/mps-youtube/yewtube/commit/c68387ea35f30aa8fa3e71e0a9941f4f43ddc9bc))

* Added branch to contrib notes ([`8dba922`](https://github.com/mps-youtube/yewtube/commit/8dba9225d1c57df3837b5d42b8523a76018e64e4))

* Bumped version number for develop ([`0003bc5`](https://github.com/mps-youtube/yewtube/commit/0003bc5fffe75673d2fa1e99a7b0cee7bc0c0976))

* Fix typo ([`c9b8420`](https://github.com/mps-youtube/yewtube/commit/c9b8420113043fc8e1afb14e5f81b366a78988a7))

* Added release date ([`f3f0fdd`](https://github.com/mps-youtube/yewtube/commit/f3f0fdd2df335f060143d0d9ce79875fc2a27fe4))

* Added album info ([`9d6a9c0`](https://github.com/mps-youtube/yewtube/commit/9d6a9c07bc64c3f1802345c96a68c5e3c7c8286d))

* renamed file ([`4bfb3f7`](https://github.com/mps-youtube/yewtube/commit/4bfb3f7774e7425da7678c5c87747e22137b2a12))

* Update version to 0.01.46 for release ([`f31b076`](https://github.com/mps-youtube/yewtube/commit/f31b07665274e77a448ce5ed3d5b62da548789cf))

* modified ([`9d72308`](https://github.com/mps-youtube/yewtube/commit/9d7230861ce368384b635a8f6400f74d642fc5e1))

* formatting ([`2168c94`](https://github.com/mps-youtube/yewtube/commit/2168c94628a4cfa5efc3219c5a686bb74d73fee5))

* Removed help from README ([`8e3570c`](https://github.com/mps-youtube/yewtube/commit/8e3570ccf9800d940ba2fa1651972868c0a4df3d))

* Formatting ([`c2a74e4`](https://github.com/mps-youtube/yewtube/commit/c2a74e42473cef7e9f2ebc23924f1e11364d04bf))

* Updated readme ([`bb13442`](https://github.com/mps-youtube/yewtube/commit/bb13442f3ae06b69ccdc2227f22006b87a509db7))

* Added launcher file ([`795f619`](https://github.com/mps-youtube/yewtube/commit/795f619214c9f94348425012279333c76317bd93))

* removed newline ([`d0ed7b1`](https://github.com/mps-youtube/yewtube/commit/d0ed7b1025468cabb55c8b72e83f9d6347597e34))

* renamed main module ([`f7d179f`](https://github.com/mps-youtube/yewtube/commit/f7d179f1527e834a4175306ed431b30b5a478df4))

* Added pin, repositioned text ([`4a816ae`](https://github.com/mps-youtube/yewtube/commit/4a816ae63faee653437559c484cf93d357426c7f))

* Updated classifiers ([`cdd376a`](https://github.com/mps-youtube/yewtube/commit/cdd376a042f9287ae0ae90a4ddab3bad1b02d570))

* repositioned import ([`eb9a4fe`](https://github.com/mps-youtube/yewtube/commit/eb9a4fe2094f10016b031c05a68c19dd5d833cc3))

* Added note on searching albums ([`61be662`](https://github.com/mps-youtube/yewtube/commit/61be662fb1a576dcbbaf56f1eaf948a8ab5240c1))

* setup as python module instead of script ([`298435e`](https://github.com/mps-youtube/yewtube/commit/298435ea1e272d60a81b4f30a656a635a1ec8cc7))

* Use console_script / entry_points ([`ec2885f`](https://github.com/mps-youtube/yewtube/commit/ec2885fdd5cbad3bb6364e0eeafb00ae72be8928))

* tidy ([`606b5a2`](https://github.com/mps-youtube/yewtube/commit/606b5a2ed72276c54265fbf5747f194a86474a4b))

* Added New Features topic to help topics
Better formatting for rating column
Added more help keywords
Added new items to help text ([`d184f6a`](https://github.com/mps-youtube/yewtube/commit/d184f6af8270038e82ca69b94f279afd80f146c8))

* Simplify &#39;set order&#39; arguments ([`fbf79d0`](https://github.com/mps-youtube/yewtube/commit/fbf79d036425a2207c4d207a23062e01f086a9a5))

* Improve logging and debugging enabling ([`ecdc9c3`](https://github.com/mps-youtube/yewtube/commit/ecdc9c3fd75682b00532068d169c63c547bfbfa8))

* Simpler fix for #78 ([`d045697`](https://github.com/mps-youtube/yewtube/commit/d045697e114788f9d2538bde512eee53d16a0fb8))

* Updated help ([`c628172`](https://github.com/mps-youtube/yewtube/commit/c628172aebdf90514acd8b6375a25f81edc90e06))

* Set max size limit for url_memo ([`ef6d616`](https://github.com/mps-youtube/yewtube/commit/ef6d616f57d6bfff0af86ba57cc2acaea93b4b24))

* Tidied unicode handling ([`136db87`](https://github.com/mps-youtube/yewtube/commit/136db8762256ae93b2bd38022b1ef5b46870ea34))

* fix encoding on artist prompt ([`a11c86c`](https://github.com/mps-youtube/yewtube/commit/a11c86c788018785a5a8c72433ce021dc2317e52))

* Replace config during album track search ([`ab0b6f8`](https://github.com/mps-youtube/yewtube/commit/ab0b6f88ca9a0b1ec2d6599579cc373c47de32f1))

* Updated changelog ([`88f8c3d`](https://github.com/mps-youtube/yewtube/commit/88f8c3db5c3e2faff5c24f9fd19c401f80bcd192))

* don&#39;t preload during album track matching ([`e9e47f0`](https://github.com/mps-youtube/yewtube/commit/e9e47f02af0657f63226fc1d55d859ae6c443bc5))

* Added album search feature ([`8540154`](https://github.com/mps-youtube/yewtube/commit/8540154fe88956906e51ae071e6659def6bfbb9f))

* Updated changes ([`37888a2`](https://github.com/mps-youtube/yewtube/commit/37888a2985f8d8f4d628add355358282e05b9715))

* Merge branch &#39;columns&#39; into develop ([`7518b36`](https://github.com/mps-youtube/yewtube/commit/7518b368ea3f79e5e89d39f998229392542af172))

* simplify column config ([`02541f2`](https://github.com/mps-youtube/yewtube/commit/02541f231677f2ab05569197e4012680737cca30))

* Add env vars to --version output ([`1f5dbba`](https://github.com/mps-youtube/yewtube/commit/1f5dbba604f57a0e8c07e417c03594ce0b2c669e))

* Show human readable numbers in search results (eg, 2.6m) ([`948b12a`](https://github.com/mps-youtube/yewtube/commit/948b12acfc5df35ace069670bf3f2db7496679d8))

* Don&#39;t terminate on EOFError opening cached url file
gh-75 and gh-72 ([`adfd095`](https://github.com/mps-youtube/yewtube/commit/adfd09584b8b6831b0a7eeb63de310ea511cc48d))

* PEP8 / tidy ([`0c9de38`](https://github.com/mps-youtube/yewtube/commit/0c9de3809fb9e253222f6c2a9b5f04d3a58fdf8d))

* Updated changelog ([`367e1ea`](https://github.com/mps-youtube/yewtube/commit/367e1eaf87f35c0a89f347775425be287c481427))

* Adjustments for larger console-width settings ([`93b7e6f`](https://github.com/mps-youtube/yewtube/commit/93b7e6f3a45f84870ef45a7b63ec9a72f0dd0745))

* Result list: shrink title before chopping from end if too much data to show ([`3e94f7d`](https://github.com/mps-youtube/yewtube/commit/3e94f7d0e3b252990e62fb5220b0d127424992e3))

* Fix for Python 3 ([`4d8ed74`](https://github.com/mps-youtube/yewtube/commit/4d8ed74d34e92c03c08a9fbcb8e96728108b18db))

* Improved custom result formatting ([`441c086`](https://github.com/mps-youtube/yewtube/commit/441c0869f5a29873e92e2f6e42ac511933c549c7))

* config console-width ([`c7df09b`](https://github.com/mps-youtube/yewtube/commit/c7df09b09f33b5e465aeb9f89695f2b6c95459df))

* Updated changelog ([`a357848`](https://github.com/mps-youtube/yewtube/commit/a35784850a4a3d4598d002eb5cbb56ddfa75acaf))

* rename viewcount to viewCount for search result format specifiers ([`4f708cb`](https://github.com/mps-youtube/yewtube/commit/4f708cb5dfa2c2e971efd72f28a3d045dfa5cfbe))

* Don&#39;t show extra fields for playlists ([`2521af7`](https://github.com/mps-youtube/yewtube/commit/2521af7c0eb3cda379fb58e1e9a0f29adc26d5bd))

* Added viewcount, dislikes and aspect (ratio) to result-format fields #64 ([`c4630c6`](https://github.com/mps-youtube/yewtube/commit/c4630c6c4f9b9fd6eed3d132d5c7b0e16d284cec))

* PEP8 ([`58b9d23`](https://github.com/mps-youtube/yewtube/commit/58b9d23c78e61010c097f841bb90cd71392ae36f))

* Added &#34;set order&#34; command (#64)

config item to specify ordering of search results.

Possible values:

set order relevance
set order published
set order viewCount
set order rating ([`6791f92`](https://github.com/mps-youtube/yewtube/commit/6791f92259a39fdb336b9f30f59e11c88096c1be))

* Optionally show video metadata with search results #64

Use the &#34;set result-format&#34; command to modify result list display

eg. &#34;set result-format {title} (by {uploader}) [{rating}] on {uploaded}&#34;

Available format codes are:

{title} - the video title
{uploader} - username of the author / uploader
{uploaded} - the video publication date
{rating} - Average rating (out of 5)
{likes} - Number of likes
{category} - The category classification of the video
{commentCount} - number of comments ([`2f9baf1`](https://github.com/mps-youtube/yewtube/commit/2f9baf1fce18914572f9cb65cdb24be0ff207eb0))

* Updated changelog ([`3d1c6e4`](https://github.com/mps-youtube/yewtube/commit/3d1c6e4d45c10be5923128e48726ca08d0e255f7))

* Tidy comments output, catch no comments ([`24a710b`](https://github.com/mps-youtube/yewtube/commit/24a710b194ed8831a32f8f4638ce8ce53c29dcbe))

* Added support for retrieving Youtube comments ([`e7f6bbd`](https://github.com/mps-youtube/yewtube/commit/e7f6bbd43f662433f06414dc403192257a69606d))

* Updated changelog ([`0a97c4b`](https://github.com/mps-youtube/yewtube/commit/0a97c4b0072b1c51bd7564a019b7a490c1b17993))

* Enable backward pafy compatibility ([`2e023dc`](https://github.com/mps-youtube/yewtube/commit/2e023dc7761ce432d5d78ad82bd1761ad89d72bf))

* Merge branch &#39;pafy0342&#39; into develop ([`75f8219`](https://github.com/mps-youtube/yewtube/commit/75f82194339f2f19e366a12c9b06f658902cffeb))

* Merge branch &#39;develop&#39; into pafy0342 ([`78c4bc6`](https://github.com/mps-youtube/yewtube/commit/78c4bc68547859e728d3cc1d98e243f2656c0cde))

* Added likes/dislikes in video info ([`4406bcb`](https://github.com/mps-youtube/yewtube/commit/4406bcb053d83d78a558e78ab741c0fab68537f3))

* Change has_known_player() to known_player_set() ([`19a8f92`](https://github.com/mps-youtube/yewtube/commit/19a8f92fafea65e75326b9cbee6eef59ea97742b))

* Don&#39;t display error message while retrying ([`2dba764`](https://github.com/mps-youtube/yewtube/commit/2dba764c2c55de3fa172a3671376e843a1be7259))

* Add published date to video info #64 ([`a6d00d2`](https://github.com/mps-youtube/yewtube/commit/a6d00d285f91d37cbb2e2929959e8420d62fef33))

* Show error for ssl stream with mplayer ([`005fad4`](https://github.com/mps-youtube/yewtube/commit/005fad4069b1416faa5c53357ccc0ad033cc8685))

* updated debug statements ([`7a3ddf4`](https://github.com/mps-youtube/yewtube/commit/7a3ddf402004488c7b20bd5d883939713ae5a040))

* Added clearcache function (for debugging use) ([`3c04280`](https://github.com/mps-youtube/yewtube/commit/3c04280a44c187e4a2b3db3fe7e21aa8348e5d08))

* Document max_res setting in interactive help

Hide show_mplayer_keys from config screen if unknown player ([`61031bc`](https://github.com/mps-youtube/yewtube/commit/61031bc48e795b6201d9ca2dc116c5e2f84ef700))

* Set version to 0.01.45 ([`859e45f`](https://github.com/mps-youtube/yewtube/commit/859e45f4060c1fffb7a551ec15ba355f8bbdcbbd))

* Tidy set config output ([`e85bf37`](https://github.com/mps-youtube/yewtube/commit/e85bf37ec3e74c4a76d5f507bc184ac73061005e))

* Update version number to 0.01.44 ([`c8735bc`](https://github.com/mps-youtube/yewtube/commit/c8735bc79adfdb7670dbcc5eaee06add8e8030dc))

* added debug statement ([`9278042`](https://github.com/mps-youtube/yewtube/commit/927804226461161f6a1ff720558a7f7ff242289e))

* catch type error in url fetch ([`8f5ed15`](https://github.com/mps-youtube/yewtube/commit/8f5ed151745f379894a752ea3e55afdf348cd9a9))

* Keep cached playlist separate from videos ([`11e55fa`](https://github.com/mps-youtube/yewtube/commit/11e55fa4180b6c51b0043637e229dc2b7cb9825e))

* Updated changelog ([`e3d8ca1`](https://github.com/mps-youtube/yewtube/commit/e3d8ca18306493935c97d41ac1ccb6a71505ce9b))

* Added window position and size config settings

More debugging output
Better error handling ([`16b0dd4`](https://github.com/mps-youtube/yewtube/commit/16b0dd4c0e36729b1060ea3ccce800c4de50f108))

* Updated changes ([`d566234`](https://github.com/mps-youtube/yewtube/commit/d566234c7a4a83314390c6b4ad14db7473e01b41))

* separate launch_player function from playsong ([`5c8d431`](https://github.com/mps-youtube/yewtube/commit/5c8d4319b33cf2e3ff919e1ac867199bf75b5526))

* Handle no matching streams found ([`1f2f41e`](https://github.com/mps-youtube/yewtube/commit/1f2f41ef0cc7cbb1d86ee0c690b7ae934e17a8a9))

* Revert to lower quality for invalid streams #65 ([`bd5da41`](https://github.com/mps-youtube/yewtube/commit/bd5da41f0c9524403f5cdf3130227a6be974202d))

* Catch EOFError on opening playlist file and report its location
for a more informative error message (#66)

Only write to playlist file when playlist items modified (#66)

Use with(open..) for all pickle loads and dumps (#66)

Add MAX_RES config item for resolution of played/downloaded videos (#56)

Cache all played url&#39;s (was only playlist items)

Cache all stream urls instead of just best audio &amp; video

Cache urls in separate file

Remove all cached urls from playlist file

Use pafy expiry property for expiring cache items

Use colours in debug statements

Set mpv as default player only if mpv found and no mplayer found

Remove redundant player flags from config
(really-quiet, fs, nolirc, prefer-ipv4) ([`722fbe0`](https://github.com/mps-youtube/yewtube/commit/722fbe0d1ffcb900c33e732b2f2fdc04b377c597))

* pylint ([`3645230`](https://github.com/mps-youtube/yewtube/commit/3645230ffb640cdba0e1b025f91cf11d482bda64))

* Updated changelog ([`20e8168`](https://github.com/mps-youtube/yewtube/commit/20e816884c4fbfeffc135ccf579156b271ff8715))

* rewrote setconfig function ([`11f5c73`](https://github.com/mps-youtube/yewtube/commit/11f5c735a374924d643702a4cc9dac654486ccb7))

* Merge branch &#39;develop&#39; into config ([`7946f11`](https://github.com/mps-youtube/yewtube/commit/7946f110158433df8677eb9ea4a0e72b1bb97a72))

* Handle &#39;video not available in your country&#39; in multiple downloads ([`4a104c3`](https://github.com/mps-youtube/yewtube/commit/4a104c3dafeb3fbe0fcb9d356de7b23c58e4b553))

* new config handling ([`28a065c`](https://github.com/mps-youtube/yewtube/commit/28a065c8ff6fbd8498474e89ee0a3a7a3e57f6e9))

* Repositioned help items ([`39982b5`](https://github.com/mps-youtube/yewtube/commit/39982b5e600c48060aefafb8b7c10d2620f04383))

* Updated help ([`8deb34e`](https://github.com/mps-youtube/yewtube/commit/8deb34e021416781f931ff69271f5fd8b3883012))

* tidyup ([`05ba728`](https://github.com/mps-youtube/yewtube/commit/05ba728e6e91182911fc6cecf19e823dfa5d6ea0))

* Don&#39;t show logo in debug mode ([`1cd9e9d`](https://github.com/mps-youtube/yewtube/commit/1cd9e9d098da527138935f4f84bed72bda29e20f))

* PLAYERARGS stored as string instead of list ([`fbb60a6`](https://github.com/mps-youtube/yewtube/commit/fbb60a66747d516a7c90c0492c8ae64538d17535))

* Simplify playerargs setting

prefer-ipv4, nolirc and really-quiet flags are added automatically when needed
they no longer appear in playerargs and are handled out of sight of the user

Similarly, the &#34;set fullscreen&#34; option no longer affects the playerargs setting
and is passed to the player behind-the-scenes if set.

Custom playerargs can still be set by the user for controlling any other
aspects of the player such as window size, geometry etc.

This makes coding the config section easier as when the user sets the player or
the fullscreen options, no other changes need to be made. ([`49bbe90`](https://github.com/mps-youtube/yewtube/commit/49bbe906eab99e16e85761691fefc0c6418b418c))

* pep8 ([`a4b3664`](https://github.com/mps-youtube/yewtube/commit/a4b3664c89fe48089e50d2eedabf2499ec611965))

* Updated changed ([`08e16d8`](https://github.com/mps-youtube/yewtube/commit/08e16d88bcc9d65e1c8f1d9367c154b587027aea))

* Add shuffle command; add &#39;edit&#39; help category; update help ([`e27b313`](https://github.com/mps-youtube/yewtube/commit/e27b3134c31b8565a4e8fb468d510982ace46180))

* Enable chained invocation commands (gh-61) ([`8f465e7`](https://github.com/mps-youtube/yewtube/commit/8f465e7ef2746079a02ec1d8282ed72028edcf65))

* Revert &#34;chain command line commands&#34;

This reverts commit 51f2564e9956b4f572f5ee98e4c4804b8d72fdee. ([`f517ca2`](https://github.com/mps-youtube/yewtube/commit/f517ca235a3ba6c3227653729166212244eb6e96))

* chain command line commands ([`51f2564`](https://github.com/mps-youtube/yewtube/commit/51f2564e9956b4f572f5ee98e4c4804b8d72fdee))

* typo (gh-60) ([`7faee02`](https://github.com/mps-youtube/yewtube/commit/7faee02df6c859df9336b914de50e8cedf1ebb6f))

* Relocate fix to issue 59 to Popen only ([`ce63a67`](https://github.com/mps-youtube/yewtube/commit/ce63a6724ea9e40d8dcc49fa403b3098f924f621))

* Update version number to 0.01.42 ([`e827d49`](https://github.com/mps-youtube/yewtube/commit/e827d4930db1f6d96c703f8a16fcbc219f7ddc3e))

* Fix encoding error for Windows with Python 2.7 (gh-59) ([`956ce80`](https://github.com/mps-youtube/yewtube/commit/956ce808c787e7521f0203ec798e0ad9f4badbc3))

* Merge branch &#39;issue58&#39; into develop ([`9a70c54`](https://github.com/mps-youtube/yewtube/commit/9a70c54c57876948a75372d9101d852ef771cb44))

* ignore unicode decode errors from mplayer output ([`fe46b5b`](https://github.com/mps-youtube/yewtube/commit/fe46b5bcd4934c28a726ee6d1fad9251d86a9f95))

* Fix formatting ([`8415c56`](https://github.com/mps-youtube/yewtube/commit/8415c56131d0c67092b8421423646da2a37ea629))

* Added release date ([`34e754f`](https://github.com/mps-youtube/yewtube/commit/34e754f9834ada603917e478f2dd5e045a8f53c9))

* Update version number to 0.01.41 ([`d294dff`](https://github.com/mps-youtube/yewtube/commit/d294dffeecf2fcb0d27d368cabaeaa3e69eb0439))

* Implemented download range with dv and da (gh-49) ([`bdda205`](https://github.com/mps-youtube/yewtube/commit/bdda2052bf81d1538439d528b74d54243c28034e))

* Fix issue with m4a audio dl with mplayer set (gh-52) ([`7ce65b7`](https://github.com/mps-youtube/yewtube/commit/7ce65b7222faea23de600dfe07294f43ecada5db))

* Documented new changes ([`de211a9`](https://github.com/mps-youtube/yewtube/commit/de211a9c0c5ddc921d8656af49f6ce742e903985))

* Merge branch &#39;youtube-id&#39; into develop ([`00c43af`](https://github.com/mps-youtube/yewtube/commit/00c43af45a7b4a8769a90c7751493c16170d5ef4))

* accept YT url or ID as argument to pl command ([`129f7e7`](https://github.com/mps-youtube/yewtube/commit/129f7e7ff5ae8aa5460ec41e44ae217eda6cab99))

* added user configurable result set size ([`62f964c`](https://github.com/mps-youtube/yewtube/commit/62f964c6845ebf8714ec9ed2ca23da7997140083))

* Added video search constrained to YT username.
&#34;user &lt;username&gt; / &lt;query&gt;&#34; ([`1ad0934`](https://github.com/mps-youtube/yewtube/commit/1ad09347016ef29210bc27eb78e8d429a37e84b5))

* v0.01.40 ([`c9cc69c`](https://github.com/mps-youtube/yewtube/commit/c9cc69c76e1e597a59c567a918b62665e445a33e))

* restore utf8 decode of Popen objects stdout ([`a00dca2`](https://github.com/mps-youtube/yewtube/commit/a00dca2889bc62663e7c934e8b9c62be2f7ad7c9))

* Revert &#34;import unicode_literals from __future__ to ease compatibility between python 2 and 3&#34;

This reverts commit 325edff682479569af6c8e21c3bc0154c1bf0fad. ([`d850a49`](https://github.com/mps-youtube/yewtube/commit/d850a49ed6887c934b485bd851938d97857df7e9))

* restore = in progress bar ([`8956d9c`](https://github.com/mps-youtube/yewtube/commit/8956d9c715d81e8498b8ebfde7ebed12e7d62e82))

* updated changelog ([`330c9b6`](https://github.com/mps-youtube/yewtube/commit/330c9b6c50f2d5156e919b80e2076f4ac98705b4))

* pylint ([`109549c`](https://github.com/mps-youtube/yewtube/commit/109549ceec5dcb2b7dc6f748cdcc48fa780c6225))

* Keep progress time format in line with listed times (99:59 -&gt; 1:40:00) ([`2568d29`](https://github.com/mps-youtube/yewtube/commit/2568d293a7b6b5ec3c1e65763c08f334b335f1df))

* use subprocess.call with mpv ([`fe535e6`](https://github.com/mps-youtube/yewtube/commit/fe535e65bf0e7e73510215583999f33905928bf0))

* Fix progress regex for mplayer -novideo &gt; 59 secs ([`6f7f608`](https://github.com/mps-youtube/yewtube/commit/6f7f608b446949c5495db2c6a5136319f390e8b5))

* Minor corrections ([`e728d18`](https://github.com/mps-youtube/yewtube/commit/e728d18fb4084a7293adf4c166c24228b814488c))

* Update version number to 0.01.39 ([`6fb0f29`](https://github.com/mps-youtube/yewtube/commit/6fb0f292d8faa981c3408a5139e85d0d73037a87))

* Documented new changes ([`3d9a135`](https://github.com/mps-youtube/yewtube/commit/3d9a135974f278b781fec80fe78cc0dea4389d23))

* progress indicator for mplayer video ([`d616970`](https://github.com/mps-youtube/yewtube/commit/d6169702336641eb0cd348d34a7542b9deab74a2))

* Merge branch &#39;develop&#39; into statusbar ([`a97e8bb`](https://github.com/mps-youtube/yewtube/commit/a97e8bb016b3d8d867674c8a5eeca9c31e6c4f21))

* Adjust row width for video list display ([`8d4ebe3`](https://github.com/mps-youtube/yewtube/commit/8d4ebe355b59e88c1f9e73fc32c900d9ef468b25))

* use YT reported video duration for progress indicator ([`d2497ec`](https://github.com/mps-youtube/yewtube/commit/d2497ec039e6113294a5c7e967a8f80bfa589f87))

* Adjust default player args ([`79e9ace`](https://github.com/mps-youtube/yewtube/commit/79e9aceb6b4bd1a89fbb7565734525ddb8220277))

* capture mpv stderr stream got extract status info ([`f57ba98`](https://github.com/mps-youtube/yewtube/commit/f57ba98ea9112bc19eec738e583f7627dc9691ee))

* display progress status for both mplayer and mpv ([`28ef410`](https://github.com/mps-youtube/yewtube/commit/28ef410876dae5355aa0eb2d2051488cffd78d90))

* Merge pull request #46 from thomasleveil/popen-non-slave/unicode_literals

import unicode_literals ([`7999cc0`](https://github.com/mps-youtube/yewtube/commit/7999cc0bf453769f31b44428a210bc5d69d9735b))

* import unicode_literals from __future__ to ease compatibility between python 2 and 3 ([`325edff`](https://github.com/mps-youtube/yewtube/commit/325edff682479569af6c8e21c3bc0154c1bf0fad))

* Merge branch &#39;pr/45&#39; into popen-non-slave ([`47f8cac`](https://github.com/mps-youtube/yewtube/commit/47f8cac9733653549bd4c73be04edf23085ef3fa))

* draw a progress bar while playing a song ([`1adb2a2`](https://github.com/mps-youtube/yewtube/commit/1adb2a2e3bb19ed2fca0ff82fc2c73080f36b34d))

* Merge branch &#39;develop&#39; into popen-non-slave ([`5c10df3`](https://github.com/mps-youtube/yewtube/commit/5c10df36893c6ce008cbe6b14c1b76e66b25f972))

* minor adjustments to help screens ([`4cdae89`](https://github.com/mps-youtube/yewtube/commit/4cdae895e446a96120ecd168a5e93fc39dd60602))

* Added help topic for configuration ([`32bdff3`](https://github.com/mps-youtube/yewtube/commit/32bdff375ebc007d5d8b72381fc750e242e5e06a))

* Merge branch &#39;develop&#39; into popen-non-slave ([`ed6f7ad`](https://github.com/mps-youtube/yewtube/commit/ed6f7ad3dd91ef8b8ec2ea147e60e51ffe3ff1b5))

* Documented changes ([`ee44c96`](https://github.com/mps-youtube/yewtube/commit/ee44c969fc24dd6ddc65753c469297ef017f23b9))

* Initialise terminal on keyboard interrupt https://github.com/np1/mps-youtube/issues/44 ([`b43bf87`](https://github.com/mps-youtube/yewtube/commit/b43bf8705ab956646d90d8527ac07710a30a552a))

* split main into two functions ([`a255f87`](https://github.com/mps-youtube/yewtube/commit/a255f878d0cf2f80c109cd33579996a6e0cc03a6))

* segmented playsong() function ([`e6b37d2`](https://github.com/mps-youtube/yewtube/commit/e6b37d22e63d8dd3ef7f018dbd0cd25c17faa4fb))

* fix view mode when using open/view in playlist display ([`6a87b88`](https://github.com/mps-youtube/yewtube/commit/6a87b888d0f5566d2a0ee5efe973dde0460805a4))

* moved inner functions to top-level ([`bdda033`](https://github.com/mps-youtube/yewtube/commit/bdda03318964a1c75d68a96043a2ec719f929622))

* Merge branch &#39;pr/42&#39; into popen-non-slave

Conflicts:
	mpsyt ([`53932e0`](https://github.com/mps-youtube/yewtube/commit/53932e07eb175d13abae2ee6c72f41dba6297f90))

* fix &#34;mplayer was not found on this system&#34; showing up when moving to next song ([`6fcd191`](https://github.com/mps-youtube/yewtube/commit/6fcd191a3349fc8080a95b3ebd413c0a781970f5))

* attempt at displaying mplayer status live - gh-38 ([`a057cf2`](https://github.com/mps-youtube/yewtube/commit/a057cf2517a574feff62a0c9fb96b1e23fdea549))

* Correction to title flag for mpv https://github.com/np1/mps-youtube/issues/41 ([`a2bf3ad`](https://github.com/mps-youtube/yewtube/commit/a2bf3adc000cb3934cd5a74d54e05c321bd7a315))

* Show content title in mplayer / mpv ([`bf99319`](https://github.com/mps-youtube/yewtube/commit/bf99319c7ab9866374288dc6ea2717e757755afe))

* tidyup ([`be78044`](https://github.com/mps-youtube/yewtube/commit/be78044f1746943b6a005489a065ccade3fd0fb2))

* remove unneeded quotes from config display ([`9e100f3`](https://github.com/mps-youtube/yewtube/commit/9e100f3166b52faf9ae1d6349af4f4e494a0c1b2))

* reordered help items ([`d1addb2`](https://github.com/mps-youtube/yewtube/commit/d1addb2a154fb2069cba77f1b064731f344946ff))

* Use // or .. to prefix playlist searches
Suppress some output when playurl and dlurl invoked from command line ([`2dbcf40`](https://github.com/mps-youtube/yewtube/commit/2dbcf40ac6e82ba4f8bbdd11e51476f3fb33196c))

* Updated changes ([`881c661`](https://github.com/mps-youtube/yewtube/commit/881c6619f5111c924b73878bf4ba82c1650fb86b))

* tidied get_default_ddir() function ([`9833627`](https://github.com/mps-youtube/yewtube/commit/98336271687bd3ef98a2cca716ca9d1ff9b8a161))

* Implemented readline persistence ([`d6ae343`](https://github.com/mps-youtube/yewtube/commit/d6ae3435a8cc874f30092aec1eef9d7e873612bc))

* Documented r{number} related video command ([`33241ef`](https://github.com/mps-youtube/yewtube/commit/33241efe7b7136d8a254dc874bc5be4c7c9044e9))

* Added command to retrieve a users playlists ([`fa85961`](https://github.com/mps-youtube/yewtube/commit/fa85961d45eeec8fbb54244e8aaba595751532b4))

* Added r{number} to retrieve related videos ([`a5743ef`](https://github.com/mps-youtube/yewtube/commit/a5743efc5e62bcaf234b835c9e7ea8e08b4a3a04))

* PEP8 ([`fbb9774`](https://github.com/mps-youtube/yewtube/commit/fbb977467e917df609b0705df2a1547ef78d41c2))

* Change 4-digit year to 2-digit in playlist search results ([`37cc44f`](https://github.com/mps-youtube/yewtube/commit/37cc44f53bad71f48e8b63230fd3ca1e3be5fe17))

* remove quotes ([`279381d`](https://github.com/mps-youtube/yewtube/commit/279381deee2583d3e9ccd961f1a0bcee9d4744a9))

* Session caching of playlist metadata
More metadata in playlist info display (i&lt;number&gt;)
Updated version number to 0.01.38 ([`5de98c8`](https://github.com/mps-youtube/yewtube/commit/5de98c8d7f89a9df4d1e50109c45520022c7ddd7))

* Changed version number to 0.01.38 ([`b35a8f7`](https://github.com/mps-youtube/yewtube/commit/b35a8f7b13881e504574b52d4346df760b5af347))

* Documented changes ([`61131fb`](https://github.com/mps-youtube/yewtube/commit/61131fb952ede0b1852dd6cddc66ac29e2d51576))

* Documented changes ([`aa51fcc`](https://github.com/mps-youtube/yewtube/commit/aa51fcc748b65caccfc6e93875397abeda95cd94))

* Implemented --debug command line option ([`878337c`](https://github.com/mps-youtube/yewtube/commit/878337c61d3eea59ae2a6df065025c3a734e3b6d))

* Don&#39;t exit playlist on HTTPError ([`b3a5bea`](https://github.com/mps-youtube/yewtube/commit/b3a5beafc4c1472cf7af3bc711bf810f0afc23db))

* Change mswinenc func name to non_utf8_encode ([`55d0e38`](https://github.com/mps-youtube/yewtube/commit/55d0e389cf8a700abdb4a87447b74b67b6593677))

* correct program name in exitmsg ([`ba607e9`](https://github.com/mps-youtube/yewtube/commit/ba607e9a105dd33fc2fcb93195319fdee286e9a8))

* adjust debugging output ([`770c970`](https://github.com/mps-youtube/yewtube/commit/770c970d623af1d5ed266fed6e73cbcbe10a648b))

* pep8 ([`eee8f7f`](https://github.com/mps-youtube/yewtube/commit/eee8f7f183fc7bb8bfc7f0ffe8a8c0b6140fd71a))

* tidy get_default_ddir() ([`72d58f1`](https://github.com/mps-youtube/yewtube/commit/72d58f10d58747b6c7e47b22a25109bcf9cad2ea))

* [Playlist info] Format dates according to locale
[Playlist info] Show update and creation dates
[Playlists results] Show update date instead of created date ([`37637a5`](https://github.com/mps-youtube/yewtube/commit/37637a5b388f1f7ac0f1f97cbe1629c34b3d2f2c))

* Tidy encoding fixes ([`8b9fb59`](https://github.com/mps-youtube/yewtube/commit/8b9fb599495ef11eb40c888765ed0fa734e82e9e))

* Fix for non-utf8 environments ([`7f31aac`](https://github.com/mps-youtube/yewtube/commit/7f31aac03780826f37adf8b3f5bd97db796ee7a8))

* Enable i&lt;number&gt; for playlist information display
playlist search results now show date (needs refining to correctly display in M-D-Y locales). ([`3b6f3d8`](https://github.com/mps-youtube/yewtube/commit/3b6f3d8b7282af58cbb130ca1eb3b13167f8374f))

* Fix url, dlurl and playurl commands when browsing playlists ([`c01dc87`](https://github.com/mps-youtube/yewtube/commit/c01dc87b441e4bc8698c23843da4abb445b8cd65))

* Fix underline ([`f94ae99`](https://github.com/mps-youtube/yewtube/commit/f94ae9996a10098b9ba15e7ec45f57e0161d1342))

* Update version info ([`400adab`](https://github.com/mps-youtube/yewtube/commit/400adab2cdf909efb0ec225fe9b153b6266cf2b1))

* Preload first result of YT opened YT playlist ([`e5d6284`](https://github.com/mps-youtube/yewtube/commit/e5d6284c536bd504b4607b1379b7d421ee8db1f4))

* Handle user input in wrong context ([`49fe9af`](https://github.com/mps-youtube/yewtube/commit/49fe9af6c87b31c47241123412bc32896338aa6b))

* minor corrections ([`2f17566`](https://github.com/mps-youtube/yewtube/commit/2f17566879b9948a1c5d9cd5b5ddfbf7ec1d30ab))

* Tidy plist function ([`ca08013`](https://github.com/mps-youtube/yewtube/commit/ca08013be26ada2e15470d1b9feeacbe711e183b))

* Adjust output for non-UTF-8 environment (https://github.com/np1/mps/issues/48) ([`160de79`](https://github.com/mps-youtube/yewtube/commit/160de79d9a53893e09b1adff07c4b5721cb78b07))

* Renamed plsearch to pls in docs ([`edb6c6d`](https://github.com/mps-youtube/yewtube/commit/edb6c6d5559786314873bdabcf2b96ee4dc9a2f4))

* Adjust playlist functionality for new pafy version. ([`18cdcd3`](https://github.com/mps-youtube/yewtube/commit/18cdcd31d094925f2f043d6185ebc2662be27329))

* Minor wording adjustments ([`4c2bfe0`](https://github.com/mps-youtube/yewtube/commit/4c2bfe0b4a58138e3ccd62f0a324f99f6025d7b7))

* added --help command line flag ([`2526076`](https://github.com/mps-youtube/yewtube/commit/25260768259f5b85389ab95e664f6fd08156d45d))

* Implemented YT playlist search and dump command ([`fa171d7`](https://github.com/mps-youtube/yewtube/commit/fa171d73a051089637ca519ed8f6a7c7b1a9fbaa))

* Added notes on new features ([`43bc0d2`](https://github.com/mps-youtube/yewtube/commit/43bc0d26076512d1ede80e925b623cfa4ebaacd4))

* Updated with new changes ([`5d6865e`](https://github.com/mps-youtube/yewtube/commit/5d6865e54553029981449966d9bbeb2e0eef485d))

* Fix formatting ([`8b47a01`](https://github.com/mps-youtube/yewtube/commit/8b47a01f3f9ed8888241a64b0fcbc6af3a481611))

* Added playurl and dlurl commands ([`bb2dad9`](https://github.com/mps-youtube/yewtube/commit/bb2dad9130569f2be176fc49f32bf243ac789495))

* Open YouTube playlist by URL ([`77eacd0`](https://github.com/mps-youtube/yewtube/commit/77eacd08e7fc6681db6ca9446ae1b8b3aab8d4d1))

* View uploads by uploader of certain item ([`dd6bb74`](https://github.com/mps-youtube/yewtube/commit/dd6bb74ed371e259377e80f2434d6f7553d63ebb))

* &#39;u &lt;number&gt;&#39; to show more videos from same user ([`60402fb`](https://github.com/mps-youtube/yewtube/commit/60402fb8ddda9ac3beb467242f6dda5121630a81))

* Added &#39;user&#39; syntax change ([`5b03eec`](https://github.com/mps-youtube/yewtube/commit/5b03eec9cac5fc4630238ee106aeed211045ce58))

* Changed docs for listing user uploads ([`53b4f3f`](https://github.com/mps-youtube/yewtube/commit/53b4f3f0842a3c6c5c2e322477be13675922cfd8))

* Changed syntax for listing user uploads to &#39;user username&#39; ([`f71bf61`](https://github.com/mps-youtube/yewtube/commit/f71bf61526e878b45858242b1a7310cf05fe07a1))

* Handle errors from accessing YT url ([`cb4528a`](https://github.com/mps-youtube/yewtube/commit/cb4528a7e314f79d1d5fee458f29c32df1180d89))

* Merge branch &#39;master&#39; into develop ([`28532c3`](https://github.com/mps-youtube/yewtube/commit/28532c351285518ceadbb59b860efa49f40e8c26))

* Merge branch &#39;develop&#39; ([`04e23f6`](https://github.com/mps-youtube/yewtube/commit/04e23f639a6faa23c6f85e62aeb473275c1f79cc))

* Added images ([`a4f7da1`](https://github.com/mps-youtube/yewtube/commit/a4f7da13396527a642c0aca4a2d2ec474fb7ebd3))

* Changed version number to 0.01.37 ([`1bdc8bb`](https://github.com/mps-youtube/yewtube/commit/1bdc8bbef7fb5e119292eb94d2bfdaaeabac788f))

* Updated with new changes ([`fc63997`](https://github.com/mps-youtube/yewtube/commit/fc639970e5d7b51cf04fe3c4213bb3fcfc06bddd))

* PEP8 corrections ([`d4ae2d9`](https://github.com/mps-youtube/yewtube/commit/d4ae2d92393a04b56c70b55dcfcec6aa502871cc))

* Separate function to generate query string. ([`a074855`](https://github.com/mps-youtube/yewtube/commit/a074855fd60aacffc4db66462a62d19637a10f4f))

* Access item by url or YT video id ([`2753b00`](https://github.com/mps-youtube/yewtube/commit/2753b00054f8e0c8a8e1bb7ec343fd97decda373))

* Add -v flag for showing version info ([`afe965b`](https://github.com/mps-youtube/yewtube/commit/afe965b341694e098e8ddb08736fcc927751db0f))

* Don&#39;t show paid content in results.

Paid content cannot be accessed from mpsyt so they should be excluded from
search results. ([`d2bb004`](https://github.com/mps-youtube/yewtube/commit/d2bb004699a0fad01bd42af1184ce4674ede6eba))

* Version 0.01.36 ([`8964ada`](https://github.com/mps-youtube/yewtube/commit/8964ada490108100b8f4ac5e4c183601c43649f4))

* Documented changes ([`1ae9751`](https://github.com/mps-youtube/yewtube/commit/1ae97510b5b19ddc7fd903aad1231c39fb5f2418))

* updated changes ([`bbf06f2`](https://github.com/mps-youtube/yewtube/commit/bbf06f2ab61d494e9db5bcf73a49f8e9443c6ee8))

* Changed some debugging messages ([`a4c353c`](https://github.com/mps-youtube/yewtube/commit/a4c353c62ad3ee3032d4eb05b8fdd551ec71e7b0))

* updated comment ([`8e41455`](https://github.com/mps-youtube/yewtube/commit/8e41455b56d00f7d6495054d331ed7c28f6f69d6))

* Carry override preference for failed playback ([`acb3e97`](https://github.com/mps-youtube/yewtube/commit/acb3e97967d0bd5e218bef5e0e9a6b56cb076e12))

* Revert &#34;Recognise webm video-only streams, offer mux&#34;

This reverts commit 7e6ae2ffbd635f290b078d993b9a8fca9f48d95c. ([`2e1aad4`](https://github.com/mps-youtube/yewtube/commit/2e1aad4161e0e6c0c7aed634d17c73589918dcbe))

* Recognise webm video-only streams, offer mux ([`7e6ae2f`](https://github.com/mps-youtube/yewtube/commit/7e6ae2ffbd635f290b078d993b9a8fca9f48d95c))

* Repositioned images ([`eb746f9`](https://github.com/mps-youtube/yewtube/commit/eb746f9fb51656b5efc9df5cebda115805a265a9))

* minor corrections ([`7a12fd9`](https://github.com/mps-youtube/yewtube/commit/7a12fd96bbe76006a20a92a102e6f08e81877350))

* corrected image url ([`8cebeb1`](https://github.com/mps-youtube/yewtube/commit/8cebeb185d443f99a13013b8f1c3b7790d07f3f3))

* Added screenshots ([`f7fb8fb`](https://github.com/mps-youtube/yewtube/commit/f7fb8fb3ff3181a3ede8baf41ed17358b6580b0d))

* wait if an item that is busy preloading is played ([`3a0e10d`](https://github.com/mps-youtube/yewtube/commit/3a0e10de8f21198826796f3e1b39d9b284c5cba8))

* Added date ([`ef7894c`](https://github.com/mps-youtube/yewtube/commit/ef7894cabef08c9ca93dfafd67f0e068ef3e73f4))

* Detailed changes ([`36d4305`](https://github.com/mps-youtube/yewtube/commit/36d4305d44f15035a4cfa345345a4ebba1a79647))

* Use audio from videostream if mplayer only has m4a (faster)
Removed -nocache from mplayer default args ([`be3d2f4`](https://github.com/mps-youtube/yewtube/commit/be3d2f456ee216968ca02f66945371067e1b6c48))

* Documented changes ([`7fca575`](https://github.com/mps-youtube/yewtube/commit/7fca575448cb3bceba2f1e91e7c2ebd1a9d63e7b))

* Version 0.01.35 ([`77766de`](https://github.com/mps-youtube/yewtube/commit/77766dee029346ef98f011bb880b03406dbaecb1))

* Maintain compatibility with current pafy version ([`48a240a`](https://github.com/mps-youtube/yewtube/commit/48a240a382a32596de4b39e50247c445e8f589c6))

* Prefer ogg when using mplayer (Better streaming) ([`14b8e80`](https://github.com/mps-youtube/yewtube/commit/14b8e80f9ea86f68452f314f8c4091a9e96b8f7d))

* reduce unnecessary data fetching ([`5cef544`](https://github.com/mps-youtube/yewtube/commit/5cef5442c1546bf570fdf7e419ba2795986bc35b))

* Fix playback delay of audio with mpv ([`d4f70a4`](https://github.com/mps-youtube/yewtube/commit/d4f70a48d062c575f047b4ad24f2c8d4eee818e6))

* v0.01.34 ([`ed1a243`](https://github.com/mps-youtube/yewtube/commit/ed1a243af9e5a92d71b92a14b0ce7ac0059ff7d8))

* Fix playlist migration attempt when no playlists exist (https://github.com/np1/mps-youtube/issues/32) ([`5a133c3`](https://github.com/mps-youtube/yewtube/commit/5a133c33b4684aaee8d085501cc79081cd747b80))

* Add release date ([`e1c48bd`](https://github.com/mps-youtube/yewtube/commit/e1c48bd7ea049502c3d63bb337a0fc893597817e))

* update changelog ([`d853b6f`](https://github.com/mps-youtube/yewtube/commit/d853b6f74f5937616bd42448fde01f56d6dccbd7))

* mux cmd now -vcodec h264 -acodec copy ([`5253b02`](https://github.com/mps-youtube/yewtube/commit/5253b02bc5699359999c2233e8cf049f2bb9f261))

* prefer avconv to ffmpeg, tidy-up, pylint, comments ([`37312f5`](https://github.com/mps-youtube/yewtube/commit/37312f5c9f8141f47c4fd1d719dd1c14208c7e7e))

* v0.01.33 ([`35452ad`](https://github.com/mps-youtube/yewtube/commit/35452adf7c2534b8e6395b7dbad565100e2a442a))

* Documented new changes ([`b796700`](https://github.com/mps-youtube/yewtube/commit/b7967006b89de96f7f3cb902667dab1d22ba558e))

* Merge pull request #31 from np1/mux

Multiplex m4v downloads with audio for more useful HD downloads ([`4b33904`](https://github.com/mps-youtube/yewtube/commit/4b33904dfc84665d307c6594165689a8ebb08515))

* Handle invalid user input in download dialog
Catch KeyboardInterrupt during mux ([`c101228`](https://github.com/mps-youtube/yewtube/commit/c1012288ce5d74d74e67ff4e8746a108b0be1b5c))

* Catch KeyboardInterrupt in download dialog ([`cc241e4`](https://github.com/mps-youtube/yewtube/commit/cc241e4f612038abc472e85dd061b6f1445537f7))

* Prompt to multiplex if m4v download selected ([`0f76cce`](https://github.com/mps-youtube/yewtube/commit/0f76cce28f1ef5f099bfdb5f90b32345ea2dc3bc))

* Fix title attribute dot notation. ([`0a56e03`](https://github.com/mps-youtube/yewtube/commit/0a56e039e58ddd666a288b61393c9f4a6e99cd8d))

* Modified debugging output ([`9f6731b`](https://github.com/mps-youtube/yewtube/commit/9f6731bd92992ff77f05cb8c55a87e077675cd1d))

* Handle failure on rental/purchase videos ([`5f99498`](https://github.com/mps-youtube/yewtube/commit/5f994985f6f31b38deb3b373f0c2be99555dc715))

* Don&#39;t pickle Pafy objects - smaller playlist file ([`cbd885d`](https://github.com/mps-youtube/yewtube/commit/cbd885d963b4287f9b7517f0383391bab869ccf1))

* Merge branch &#39;master&#39; into develop ([`6446502`](https://github.com/mps-youtube/yewtube/commit/64465025df14dc48bd478c6992c955b8d485697d))

* correct quoting for rst ([`7f0feac`](https://github.com/mps-youtube/yewtube/commit/7f0feac638b72a14672f0e5f034217982ed4db2d))

* Merge branch &#39;master&#39; into develop
updated README files for notes on fullscreen and show_video ([`942e069`](https://github.com/mps-youtube/yewtube/commit/942e069bbceef1612fc9278682461609c8e325e3))

* Expand notes for set fullscreen and set show_video ([`9633d12`](https://github.com/mps-youtube/yewtube/commit/9633d12aa9c61717282e39f034836c9e2a9eeb6e))

* Minor changes for pylint ([`bbf315e`](https://github.com/mps-youtube/yewtube/commit/bbf315eaf9f6718f36ec4a4a21c672640dc1f10d))

* Preload now fails silently (https://github.com/np1/mps-youtube/issues/27) ([`9271c07`](https://github.com/mps-youtube/yewtube/commit/9271c07040f019bb5b2e608962ded1274a58d3cc))

* Set version number to 0.01.33 ([`a23d4c9`](https://github.com/mps-youtube/yewtube/commit/a23d4c95262e498bde9b6c239a452159f8510ff3))

* Set width of EA ambiguous chars to 1 to correct alignment of Russian text ([`1c33b54`](https://github.com/mps-youtube/yewtube/commit/1c33b54708fdef454f895a43e979c0009c90149f))

* added CHANGELOG file (https://github.com/np1/mps-youtube/issues/28) ([`979de19`](https://github.com/mps-youtube/yewtube/commit/979de19dbc2f4cdec6dbb509586db201f726eca3))

* Version 0.01.32 ([`5b7e830`](https://github.com/mps-youtube/yewtube/commit/5b7e8308b933cef68f9a71c170bb57a9e9edfbdd))

* Merge branch &#39;master&#39; of https://github.com/np1/pms-youtube into developtest ([`f43aad5`](https://github.com/mps-youtube/yewtube/commit/f43aad5d7531df0cf90cfd205c3a977167956ee0))

* Merge pull request #29 from thomasleveil/fix/showconfig-fail-win32

Fix crash when using the &#39;set&#39; command on Windows ([`849a4e4`](https://github.com/mps-youtube/yewtube/commit/849a4e4dcf2453bcc27a13deee26aa31d5a6c97d))

* Fix crash when using the &#39;set&#39; command on Windows ([`1cf4f2b`](https://github.com/mps-youtube/yewtube/commit/1cf4f2b607bca2fe73859de5b4e127a465b4d093))

* Don&#39;t modify pafy Stream object
correct rpad item title ([`2b135ed`](https://github.com/mps-youtube/yewtube/commit/2b135ed14e8caedbf5eac6b5a215f3121102c5d4))

* Change debug env var name ([`aae9a5e`](https://github.com/mps-youtube/yewtube/commit/aae9a5e7a53c023cc26898ae7f0db875e15f9f22))

* Correct width for certain unicode chars ([`34f0435`](https://github.com/mps-youtube/yewtube/commit/34f0435f7b370b6a57255a93ecaa2b8f50b304d8))

* Bump version to 0.01.31 ([`d4b784e`](https://github.com/mps-youtube/yewtube/commit/d4b784e98db2f156b1f82419ae1f307e742f9e26))

* Migrate conf dir to mps-youtube ([`d4badad`](https://github.com/mps-youtube/yewtube/commit/d4badadcf41c0820b9ead3d953cd48e828317310))

* modify logo function for better vim folding ([`ae70d4d`](https://github.com/mps-youtube/yewtube/commit/ae70d4dc68803728879759d1e71535fd0c49a8c9))

* Merge branch &#39;develop&#39; ([`733eaa0`](https://github.com/mps-youtube/yewtube/commit/733eaa080e7b65102f54ac8cd6f91d2cbd619652))

* Changes for new name ([`8f82727`](https://github.com/mps-youtube/yewtube/commit/8f827270dcacaebe30c337d97f50121ad1ffd9ce))

* Remove logo from readme ([`d644cb9`](https://github.com/mps-youtube/yewtube/commit/d644cb9909ee21a1352e559782adc6159a4763ed))

* Update notes to fit new name ([`aa7d366`](https://github.com/mps-youtube/yewtube/commit/aa7d3663b0978a19c4809a4bdfe52118978815de))

* Renamed main python file to mpsyt ([`2463a05`](https://github.com/mps-youtube/yewtube/commit/2463a0596f586b267c40f2b2e31af899c6a19ae8))

* More rebranding ([`d0ed349`](https://github.com/mps-youtube/yewtube/commit/d0ed349b9078cf39716b8894bfe7af4afcb2d465))

* Rebrand to mps-youtube ([`0708a4f`](https://github.com/mps-youtube/yewtube/commit/0708a4f9265dc5087d9836005627cee8d830479d))

* new name ([`ee4e04b`](https://github.com/mps-youtube/yewtube/commit/ee4e04bb98396f20ef013032032e748321e20cd0))

* Renamed main file ([`48ea019`](https://github.com/mps-youtube/yewtube/commit/48ea019313aca6c785aec515f35dfddf8f9c38a9))

* Add note about project rebrand. ([`e2304b0`](https://github.com/mps-youtube/yewtube/commit/e2304b0c3a032d2b3bc8e0375699ad68440f8379))

* more rebranding ([`d77b869`](https://github.com/mps-youtube/yewtube/commit/d77b8699bfb427f5e87fc1363a03fe8b893d09ac))

* partial rebranding to mps-youtube ([`84ea82e`](https://github.com/mps-youtube/yewtube/commit/84ea82e557a3c1c9a4b4c2c302543a19c82dc3e2))

* replace pyutf8_decode for default download dir ([`084367b`](https://github.com/mps-youtube/yewtube/commit/084367bc8c165d185fb6de5cae66c5564be91a04))

* v0.01.13 ([`a17827f`](https://github.com/mps-youtube/yewtube/commit/a17827f4ded4cd1a420c626724bbaf4dbbae5f28))

* Divide search function ([`be468cb`](https://github.com/mps-youtube/yewtube/commit/be468cbbc565b936f76d5ede73c69bd67a21cfd4))

* Move text strings info function ([`5ba4999`](https://github.com/mps-youtube/yewtube/commit/5ba4999ae1c524605dd525871132d9eeba69e334))

* add .py ([`031dbef`](https://github.com/mps-youtube/yewtube/commit/031dbefe225d556be2fdf9ee605874f943d906a4))

* Fix alignemnt for large filesizes in download menu ([`cd9fbcf`](https://github.com/mps-youtube/yewtube/commit/cd9fbcfc4e17f01e43319c78b8ff1f6cb0a68701))

* Add notes field for download streams ([`4715412`](https://github.com/mps-youtube/yewtube/commit/47154123ea3ed9b99571024c743a79eea9d0b908))

* Play audio using video stream as fallback (fixes https://github.com/np1/pms-youtube/issues/7) ([`14cb179`](https://github.com/mps-youtube/yewtube/commit/14cb179b3ceefd600a3dd2c86049f7b1f7306c80))

* typo ([`2728a85`](https://github.com/mps-youtube/yewtube/commit/2728a853e5a0e005e67fac22e9588c1c2ef77d8c))

* Tidy builtin help ([`338da11`](https://github.com/mps-youtube/yewtube/commit/338da114623815c9539b52e9586bc1e56bc5e59c))

* fix kwargs = () ([`820f3d3`](https://github.com/mps-youtube/yewtube/commit/820f3d351a2d860e10b86a91b710394e2928465b))

* Fix spacing on help item ([`89a42cb`](https://github.com/mps-youtube/yewtube/commit/89a42cb08ede9d7528fb8ca714bee8b7842c264c))

* Set showvideo default to false (https://github.com/np1/pms-youtube/issues/23) ([`9d585f9`](https://github.com/mps-youtube/yewtube/commit/9d585f9c23b8b382be9676265f75ceade0292041))

* v0.01.12 ([`8971edc`](https://github.com/mps-youtube/yewtube/commit/8971edc8ad2463bca73a1f3e97eb6d8a3d03b568))

* Document new dl options ([`2082a4b`](https://github.com/mps-youtube/yewtube/commit/2082a4bb163647632c77d3258021ca4fe3142675))

* dv&lt;num&gt; and da&lt;num&gt; to dl best video/audio ([`5338419`](https://github.com/mps-youtube/yewtube/commit/5338419b7de9d064fbde6ad9a28b8dfb7a14ba14))

* Format adjustments ([`44af78b`](https://github.com/mps-youtube/yewtube/commit/44af78b98ccf3d504976762e63deb93c4fecc9e7))

* pep8, pep257 ([`4cce665`](https://github.com/mps-youtube/yewtube/commit/4cce665093eef070212a7520a37938a3d2545666))

* New download menu to select formats ([`48d9d7a`](https://github.com/mps-youtube/yewtube/commit/48d9d7ae4dcbd9e40e517007dd81cc6c598d3007))

* Remove debugging print statement ([`2b8b7d2`](https://github.com/mps-youtube/yewtube/commit/2b8b7d2649de47d0275b4def9076e144aa897f52))

* smaller try/except block in play_range ([`d0fab8c`](https://github.com/mps-youtube/yewtube/commit/d0fab8c78b36c6424d8cd96cf510d998ee86970c))

* v0.01.11 ([`360266b`](https://github.com/mps-youtube/yewtube/commit/360266b7ad4eb9452f0ef29129483da172b36033))

* Update config files from versions &lt;= 0.01.08 ([`538c482`](https://github.com/mps-youtube/yewtube/commit/538c4821c7fe2779ee39ea5c4d97bcfba8b96d7a))

* Smaller try/except block for playsong ([`e608f05`](https://github.com/mps-youtube/yewtube/commit/e608f053a254507255b1be3ee02e53de185f220b))

* v0.01.10 ([`87bb816`](https://github.com/mps-youtube/yewtube/commit/87bb81643de6656031d989339a0183d182642f5d))

* fix ddir default config ([`d60f094`](https://github.com/mps-youtube/yewtube/commit/d60f0945cdb27379e125860c69d24666ca302e97))

* tidy display config override code ([`519637d`](https://github.com/mps-youtube/yewtube/commit/519637d364d5cfa944fa2e4b0a1237a97919f04c))

* tidy config ([`361d705`](https://github.com/mps-youtube/yewtube/commit/361d705e504af4b4f2ac9a7a9c4409dbad765f4c))

* fix config ([`67a6443`](https://github.com/mps-youtube/yewtube/commit/67a6443d7d4809a089dc550c78d87589dd45113e))

* Fix fullscreen default config ([`3a51159`](https://github.com/mps-youtube/yewtube/commit/3a51159dbc992ead5fff640d44e40acb8b85e322))

* Fix duration field alignment ([`1ff75ba`](https://github.com/mps-youtube/yewtube/commit/1ff75ba7ed496aa687b484e0bef7be8cd1ecf230))

* Update config instructions ([`3001c43`](https://github.com/mps-youtube/yewtube/commit/3001c4316d100ac8be8a3481c1a22b68cf47a57b))

* Implemented override of playback options
New fullscreen setting ([`2ddb56f`](https://github.com/mps-youtube/yewtube/commit/2ddb56f12c8d935130e6531edeaa341ef7efc85f))

* Bump version number ([`8b8dead`](https://github.com/mps-youtube/yewtube/commit/8b8deadc92f94982985fdd9567b82e75208a36c4))

* Use a list for help screens ([`2d3ae0f`](https://github.com/mps-youtube/yewtube/commit/2d3ae0f4bd56dcb956c347db63b50a6d7d80bb7c))

* Repositioned some help items. ([`6ef04ae`](https://github.com/mps-youtube/yewtube/commit/6ef04ae4dd89033221d5043ffcd5e54857933634))

* &#39;help&#39; prompt in help mode ([`597603e`](https://github.com/mps-youtube/yewtube/commit/597603e0d60232c4c994753c320575fe8e7790ad))

* Remove unused userinput variable ([`8882434`](https://github.com/mps-youtube/yewtube/commit/8882434eca696ba53ef3f06c588eb9265376dfe2))

* Use http instead of https
don&#39;t use input as a variable name (renamed to inp) ([`a8532b0`](https://github.com/mps-youtube/yewtube/commit/a8532b024529d9a10d19d840f301d8345a51b0c7))

* Merge branch &#39;master&#39; of https://github.com/ainola/pms-youtube into ainola ([`9cd4205`](https://github.com/mps-youtube/yewtube/commit/9cd4205ed6cedb7fd6348cdf65dc169f78bad36b))

* added help section for invocation, fixed spelling ([`0a092cf`](https://github.com/mps-youtube/yewtube/commit/0a092cf5bdecf5916e436f3373869ca928c0fa1f))

* made the help more extensive ([`0b66733`](https://github.com/mps-youtube/yewtube/commit/0b6673365d6bb035cb060702077564808eae4ba9))

* reverse my changes to time display; fixed upstream ([`b5f5c49`](https://github.com/mps-youtube/yewtube/commit/b5f5c4993f2694ded4354b409555d6f030ca5bda))

* proper display for lengths greater than 59:99 ([`7558f6f`](https://github.com/mps-youtube/yewtube/commit/7558f6fe4b0e5ba253064efe237245edae6b29f4))

* Use http instead of https ([`56fb684`](https://github.com/mps-youtube/yewtube/commit/56fb684b3411b31d2486cfcb23c3332513d61bab))

* Fix Length field alignment ([`2dc741f`](https://github.com/mps-youtube/yewtube/commit/2dc741f2ac6159059534fb24232a194de321e32a))

* Merge branch &#39;master&#39; of https://github.com/np1/pms-youtube ([`eef7bdc`](https://github.com/mps-youtube/yewtube/commit/eef7bdc24f214dfed729a6a54f82ae669c8a8b57))

* Merge pull request #11 from ainola/master

Add help entry for showing info of result. ([`54484e4`](https://github.com/mps-youtube/yewtube/commit/54484e4dc303da0741245c3cb4d4153f85722c90))

* Add help entry for showing info of result. ([`1febfa5`](https://github.com/mps-youtube/yewtube/commit/1febfa526cae3914fa33c5920078ba3728e79f01))

* use env variable for debug logging ([`c8da757`](https://github.com/mps-youtube/yewtube/commit/c8da757348012bf1ae566929dbfe8a1e0b153821))

* Increase retry count ([`ce34c95`](https://github.com/mps-youtube/yewtube/commit/ce34c95c99fda167dd1595769c555a9aee0f7b99))

* Fix display of items longer than one hour. ([`2409eb5`](https://github.com/mps-youtube/yewtube/commit/2409eb5f5993a252fc961e9ab33bac12f98d6dc9))

* v0.01.08 ([`1ed8260`](https://github.com/mps-youtube/yewtube/commit/1ed8260a43adbc7c76c8d26928db3b1d070360ed))

* PEP8, PEP257 ([`5ceb72c`](https://github.com/mps-youtube/yewtube/commit/5ceb72c4764e315d31e1d2f6c81ba8f04b9d8a61))

* Set mpv on first run if found in path ([`c3fb471`](https://github.com/mps-youtube/yewtube/commit/c3fb47156bf7aa1721075663e7d8bf4589aa25f1))

* allow * in item selection ([`1d94650`](https://github.com/mps-youtube/yewtube/commit/1d9465094bcd14d47faeb22021698c7940a1862d))

* Use &#39;*&#39; where &#39;all&#39; can be used ([`3aefb36`](https://github.com/mps-youtube/yewtube/commit/3aefb360ca0454e04c0e3fd656fe3d5b14530f02))

* Don&#39;t log to screen ([`b97e4fe`](https://github.com/mps-youtube/yewtube/commit/b97e4fed3bbf7d25f4bb72d2ef3267f477b85eae))

* Added stream url pre-fetching ([`0a45999`](https://github.com/mps-youtube/yewtube/commit/0a4599949c7db2bf7bdd9b5f264154e8a71dcf5d))

* 0.01.07 ([`295a4b4`](https://github.com/mps-youtube/yewtube/commit/295a4b4bd9eae96e958ef32997fd70e17495904e))

* tidy playsong and download functions ([`b451e76`](https://github.com/mps-youtube/yewtube/commit/b451e76a18748f5cdea258caafb2b381fd2413c5))

* store pafy object in results ([`d6eb23a`](https://github.com/mps-youtube/yewtube/commit/d6eb23ae1d8527763942d40c386760099c26fc73))

* strip newline ([`87790fa`](https://github.com/mps-youtube/yewtube/commit/87790fa9b3e256dcee1bcbe423efc5c36650494f))

* add ignore file ([`20ad5b2`](https://github.com/mps-youtube/yewtube/commit/20ad5b2885be276938f15b14f79cc50ca921cad7))

* Typo fix, fix for python3, additional check for ~/Downloads

Conflicts:
	pmsyt ([`8234fcf`](https://github.com/mps-youtube/yewtube/commit/8234fcf8e42029b028c29b27805c94498677c256))

* Fix playlist display conditions ([`6019164`](https://github.com/mps-youtube/yewtube/commit/6019164f1305cdc482d1f50f87de417874f565fd))

* Better storing of used links ([`f402d26`](https://github.com/mps-youtube/yewtube/commit/f402d2611df7536dd6b825d76f8a0731b68f9096))

* update version number ([`e5645ad`](https://github.com/mps-youtube/yewtube/commit/e5645ad4d608212a58f99e88d6071fb7b4d4b7e8))

* Added ignore files ([`4a2e9c1`](https://github.com/mps-youtube/yewtube/commit/4a2e9c17a15f1f6bb65ea48cd2ec7650e083205f))

* Add notes for getting users videos ([`d8ab361`](https://github.com/mps-youtube/yewtube/commit/d8ab361e8379efc7b0a863e8756da90b97a47dcc))

* fix encoding of video metadata ([`0a0409d`](https://github.com/mps-youtube/yewtube/commit/0a0409db5e393412789ef1982d91fb44f7bef996))

* Format metadata ([`6acc7ce`](https://github.com/mps-youtube/yewtube/commit/6acc7ce9b226ad68cd45e7f9ebd827043cb269a3))

* Get yt user uploads with -user ([`cf0bf79`](https://github.com/mps-youtube/yewtube/commit/cf0bf790d38ec0b7f97c7ed30e7478153753eda9))

* simplify setting config ([`838bbdd`](https://github.com/mps-youtube/yewtube/commit/838bbdd320077ebe070f271cd18324fd257db3ee))

* README.rst

Simpled setting config ([`d1e4582`](https://github.com/mps-youtube/yewtube/commit/d1e4582c71b999da4ce2bc34917d9e6314a1e4a1))

* simplified change config ([`5f2c550`](https://github.com/mps-youtube/yewtube/commit/5f2c5503b55feb11b662936b5b10b652cc3533e4))

* Remove top tracks notes ([`5415ed7`](https://github.com/mps-youtube/yewtube/commit/5415ed73b846c1751a22ad16765355ba7abda5f3))

* Instructions for fullscreen mode ([`ca38dea`](https://github.com/mps-youtube/yewtube/commit/ca38deaa0e3d4320b02e3270c0e828bf3b1496ef))

* Handle no search results ([`5f72479`](https://github.com/mps-youtube/yewtube/commit/5f72479e87732aee8b475b73c253df2563ae8202))

* Fix category search ([`1c6f81b`](https://github.com/mps-youtube/yewtube/commit/1c6f81bcad8abc50963981e49896cb0a009981b7))

* 0.01.03 ([`17ac462`](https://github.com/mps-youtube/yewtube/commit/17ac4621d631914207fbfae50bac746efb94999e))

* remove print url ([`50aedcb`](https://github.com/mps-youtube/yewtube/commit/50aedcb90bdad41bd1d636d57154051a45de23ad))

* fix start page ([`03ffe22`](https://github.com/mps-youtube/yewtube/commit/03ffe224583859e966cfef4b610272abe73bc676))

* Fix badge url ([`5fc22a1`](https://github.com/mps-youtube/yewtube/commit/5fc22a1e3358dc63cd564ed44263a88a51ae17db))

* fix link ([`36bdbf3`](https://github.com/mps-youtube/yewtube/commit/36bdbf3df56ed131163d29146e8833c78a80bcc6))

* Change version number ([`a19b5f1`](https://github.com/mps-youtube/yewtube/commit/a19b5f1c8af78a938f079c025a656d02a7844f08))

* added .gitignore ([`8bc7bfc`](https://github.com/mps-youtube/yewtube/commit/8bc7bfc4fb3f704cb00488659494eba4662b31aa))

* missing comma ([`fe1f008`](https://github.com/mps-youtube/yewtube/commit/fe1f0081eb7a382580e4a7f6ce4107f59a544e9d))

* change depends info ([`b53cd64`](https://github.com/mps-youtube/yewtube/commit/b53cd64dbd6f8679090fa5bc5f9e9e607595ef5c))

* add pafy requirement ([`de8a7bd`](https://github.com/mps-youtube/yewtube/commit/de8a7bd7bbeee741320f5faea974ba7aafad9f80))

* Use OS default config dirs ([`4a3d5ff`](https://github.com/mps-youtube/yewtube/commit/4a3d5ff4ba593f96e0371e5d2c8cc4d834908e0b))

* Updated install notes. ([`70b999b`](https://github.com/mps-youtube/yewtube/commit/70b999b52f945da6ec976419619f9bd9ede2a22a))

* Updated docs. ([`f17a186`](https://github.com/mps-youtube/yewtube/commit/f17a18631d2667e84b1f623f65a1e1fbfea8a9c7))

* Updated notes. ([`a93ffb6`](https://github.com/mps-youtube/yewtube/commit/a93ffb68a9c7806d230d718e629cba9ce147351f))

* yt specific changes ([`8997010`](https://github.com/mps-youtube/yewtube/commit/89970109594c9707a794e193d1c5ff936f23e37a))

* yt specific changes ([`dd65764`](https://github.com/mps-youtube/yewtube/commit/dd657643635e23cc3ac520d3847166f2662febd8))

* added CONTRIBUTING notes. ([`999fe1e`](https://github.com/mps-youtube/yewtube/commit/999fe1e426bcc88198ab427d21f686178f4e38dc))

* Set version ([`27566e3`](https://github.com/mps-youtube/yewtube/commit/27566e31762eb6645d91709b8eebfc0bab9725b7))

* Changes for YT ([`c9edf06`](https://github.com/mps-youtube/yewtube/commit/c9edf066dccf432c85466d7a6c94d2a86c9c6077))

* More YouTube specific changes. ([`cb609b7`](https://github.com/mps-youtube/yewtube/commit/cb609b75b35c8ee4cfe1711f39dfa033e653089b))

* YT specific changes ([`955487a`](https://github.com/mps-youtube/yewtube/commit/955487a3dc8ef4e1a3d2d775f11b747a7d04db35))

* Updated for YouTube ([`de45b42`](https://github.com/mps-youtube/yewtube/commit/de45b4222d9bcfef4f14805f75ba85600e27cd51))

* Use YouTube backend ([`6f5e7a3`](https://github.com/mps-youtube/yewtube/commit/6f5e7a3c64358a58400a2581c5b1567cce925488))

* Use VERSION file to check version ([`d6568db`](https://github.com/mps-youtube/yewtube/commit/d6568db9a1e1997b98fff54079f69cf070d4b637))

* reset version number ([`aa1a58d`](https://github.com/mps-youtube/yewtube/commit/aa1a58dec893d37ddfbbd411ff8ad07689229b84))

* Smaller file for update checks ([`889e622`](https://github.com/mps-youtube/yewtube/commit/889e6225e5ed994874a6c10adaeae1837569909f))

* redirect stderr for mpv ([`a194da0`](https://github.com/mps-youtube/yewtube/commit/a194da097743dcab3c23a8c4ac86d15ec50ab261))

* bump pypi version number ([`30ad01c`](https://github.com/mps-youtube/yewtube/commit/30ad01c006c6e2f09d467e305b5e7c88fb572161))

* Add notes for using mpv ([`c799b94`](https://github.com/mps-youtube/yewtube/commit/c799b946e9496c02e8e387aa7184ff5766ff0a5d))

* change __dict__ to getattr ([`2db0748`](https://github.com/mps-youtube/yewtube/commit/2db0748247079fac8b0e0d1f11514fa3a8e7ca9b))

* Remove pypi badge ([`bdfe702`](https://github.com/mps-youtube/yewtube/commit/bdfe702cc6d29e3128dcc30e5d2a06e9cdc2c585))

* move PLFILE out of Config ([`26e1ef6`](https://github.com/mps-youtube/yewtube/commit/26e1ef625a80c522f2ea59e03f592c783e595f67))

* Use different versioning for PyPI ([`4ab6a32`](https://github.com/mps-youtube/yewtube/commit/4ab6a32436b2b878f42ed359794d7fbd84483e98))

* Get config params from Config class ([`df6eda1`](https://github.com/mps-youtube/yewtube/commit/df6eda11c9388f64c140a4db929834bd0d139457))

* Revert &#34;Revert &#34;Get conf params from dir(Config)&#34;&#34;

This reverts commit b912ff4154f358bb1a02c5c1e3ee090720fd9fc1. ([`c8ea841`](https://github.com/mps-youtube/yewtube/commit/c8ea8413a7fa6d99ed4dba6f2ced0ee6a69c7966))

* Revert &#34;Get conf params from dir(Config)&#34;

This reverts commit a22f512f7ba4a947002f5072ab68dcdfc1ba768a. ([`b912ff4`](https://github.com/mps-youtube/yewtube/commit/b912ff4154f358bb1a02c5c1e3ee090720fd9fc1))

* Get conf params from dir(Config) ([`a22f512`](https://github.com/mps-youtube/yewtube/commit/a22f512f7ba4a947002f5072ab68dcdfc1ba768a))

* tidy current song display ([`cf37bc1`](https://github.com/mps-youtube/yewtube/commit/cf37bc16d1cec2e7a0d67be7d7ffcab3eb5a4747))

* Nicer layout for single song play ([`2fd480f`](https://github.com/mps-youtube/yewtube/commit/2fd480fc900e983830e4f8c622552f8a2bf26102))

* remove unused parameter ([`a6429fe`](https://github.com/mps-youtube/yewtube/commit/a6429fef2010e551b494cdbf673bb10f80219ab6))

* v0.18.38 ([`a614bce`](https://github.com/mps-youtube/yewtube/commit/a614bceb96f4b19fda91b7ebb59dc55c39ee3012))

* v0.18.38 ([`3ddbba0`](https://github.com/mps-youtube/yewtube/commit/3ddbba08b178e9f51d1d1d1981635feb8960d66f))

* Fix default windows colour option ([`e842593`](https://github.com/mps-youtube/yewtube/commit/e8425936f2b214ee27ba06e1305d2e4aa7fea0c8))

* Rename py2utf8 function ([`0d6f7cd`](https://github.com/mps-youtube/yewtube/commit/0d6f7cd1f1a7c8f954089f395d86b356b6eaf220))

* Merge branch &#39;master&#39; of https://github.com/np1/pms

Conflicts:
	pms ([`579d1f1`](https://github.com/mps-youtube/yewtube/commit/579d1f1e4eea18819e12481d46f121ec6a79b96e))

* Show duration of playing song ([`50a928a`](https://github.com/mps-youtube/yewtube/commit/50a928a9677025a95b4bd8ae8c4036a61a12983b))

* tidy config line ([`962c04f`](https://github.com/mps-youtube/yewtube/commit/962c04fa7579615e257b0b99240bc7fc51a6b60f))

* Minor corrections ([`078c5da`](https://github.com/mps-youtube/yewtube/commit/078c5da9c61eb9efbb5a387150c3ecdf545956fe))

* Show duration of playing song ([`ced956d`](https://github.com/mps-youtube/yewtube/commit/ced956d8f06cc408beef478962dd3da62bd8600c))

* Fix broken setconfig ([`e3130cd`](https://github.com/mps-youtube/yewtube/commit/e3130cd9580979c8d7d7b5a24434635b2e3c3ef1))

* Remove extra newlines ([`8940a4c`](https://github.com/mps-youtube/yewtube/commit/8940a4c5d0a87e81c225b4a1551a750ce02ad32b))

* Show songlist instead of logo on single track play ([`8cb7ecf`](https://github.com/mps-youtube/yewtube/commit/8cb7ecfdf86993f74c727adf898cb126f1c318fa))

* Merge branch &#39;master&#39; of https://github.com/np1/pms

Conflicts:
	pms ([`aef0c26`](https://github.com/mps-youtube/yewtube/commit/aef0c269d1738925bcb2cb32f0436b3198021b1b))

* Add option to hide mplayer keys ([`3ea3c1f`](https://github.com/mps-youtube/yewtube/commit/3ea3c1f55af0ad9340f19cf1e824bf15603b0e71))

* Add option to hide mplayer keys ([`587c493`](https://github.com/mps-youtube/yewtube/commit/587c4935bf63b03f97dfd8c7e0ff59ecdcaf5529))

* Disallow colours on Windows without colorama ([`994c928`](https://github.com/mps-youtube/yewtube/commit/994c928e01a9f576fac0ee6d9581d9b129a2244e))

* Updated Windows install notes. ([`82bf05c`](https://github.com/mps-youtube/yewtube/commit/82bf05c5464123e4f7db4835bbf8226ecc4bfd8b))

* change filemode to 755 ([`2be03fd`](https://github.com/mps-youtube/yewtube/commit/2be03fd5654f7fdee6904f1fd05de03c1c8eb1e2))

* Fix colours on Windows ([`5d9feda`](https://github.com/mps-youtube/yewtube/commit/5d9feda4132c6a784e9c15830d27210cc5cab8b5))

* v0.18.37 ([`5b351e3`](https://github.com/mps-youtube/yewtube/commit/5b351e31c528f159286639dbf5f4f07f890e2401))

* Expanded Windows installation notes ([`ac7f372`](https://github.com/mps-youtube/yewtube/commit/ac7f3725521836b85a874cca28b18aedec40726e))

* Fix prompt for Windows ([`dc41824`](https://github.com/mps-youtube/yewtube/commit/dc418246aab2429eb5cc81afbd8623abe610309e))

* Windows display fixes ([`ce604ac`](https://github.com/mps-youtube/yewtube/commit/ce604ac4050d81915bf4539860fb85d914023511))

* Fix mplayer key help on Windows ([`0889318`](https://github.com/mps-youtube/yewtube/commit/0889318c71a9e6f38bcd7bcbc626cb499ecdb85f))

* 0.18.36 ([`08e4fbf`](https://github.com/mps-youtube/yewtube/commit/08e4fbf3fb79c8967ccbde6a7a1d9b791a18df76))

* Merge branch &#39;master&#39; of https://github.com/np1/pms ([`ae48bc7`](https://github.com/mps-youtube/yewtube/commit/ae48bc73302abd7468f9e1d184785b92888aa10b))

* Merge pull request #30 from thomasleveil/windows_colors

add color support for Windows ([`621aa86`](https://github.com/mps-youtube/yewtube/commit/621aa86dabdebd71fa883e636bf4f2c096ce121a))

* add optional color support for Windows

if the colorama python module is found ([`a4409d8`](https://github.com/mps-youtube/yewtube/commit/a4409d87cad9a6c6feeb71f5f18e7b9d2779ae63))

* Cleaner prompt ([`c8fbf7f`](https://github.com/mps-youtube/yewtube/commit/c8fbf7fdbea8529ece028adc420173c57252fa9c))

* Allow / as search prefix ([`afa4c62`](https://github.com/mps-youtube/yewtube/commit/afa4c621c32a1b450460b6c024189f9d0bed2234))

* Use setuptools, fallback to distutils.core ([`a03e034`](https://github.com/mps-youtube/yewtube/commit/a03e034e5404f975f71e10e139cc7d6e4f8db7ba))

* v0.18.35 ([`5f5358f`](https://github.com/mps-youtube/yewtube/commit/5f5358f82b82606b488549be7fd1f1a0d84eb188))

* Replace / in filename.  Fixes https://github.com/np1/pms/issues/31 ([`67c81be`](https://github.com/mps-youtube/yewtube/commit/67c81bebb4f856bb067936e2015720abc4b08290))

* tidied help text.
catch socket timeout ([`9f3ca24`](https://github.com/mps-youtube/yewtube/commit/9f3ca24fee14ebc1f5adc8f2daab77656c0bc844))

* v0.18.34 ([`2cf37a0`](https://github.com/mps-youtube/yewtube/commit/2cf37a0ca3652c7f48a9b4309fc3b034c300aaef))

* handle bad json data ([`1726c1b`](https://github.com/mps-youtube/yewtube/commit/1726c1b8dfdcd70dca05ff0965410167d5ee55f2))

* v0.18.34 ([`3ba3374`](https://github.com/mps-youtube/yewtube/commit/3ba3374b366d4e38c8fa2552d73092709c1fa188))

* fix for no JSON object error ([`dfda59d`](https://github.com/mps-youtube/yewtube/commit/dfda59d85db600788b766a188b836ca4e4e70b09))

* v0.18.33 ([`c26deea`](https://github.com/mps-youtube/yewtube/commit/c26deea38365876318663ce62b55e837e183297b))

* v0.18.33 ([`e4a3d89`](https://github.com/mps-youtube/yewtube/commit/e4a3d89ae6dec57a584cd05f94597dc97c38d3a9))

* 0.18.32 ([`6747bd1`](https://github.com/mps-youtube/yewtube/commit/6747bd1df83b763cbac8dbc20573e0c028b35591))

* Re-add playlist import command ([`cdbf05f`](https://github.com/mps-youtube/yewtube/commit/cdbf05f838149f9c2df0e587a65dcc0e89ea539e))

* Document playlist import command ([`3ddad8b`](https://github.com/mps-youtube/yewtube/commit/3ddad8b21f89ba893b9b2ada80d43b1b148384cd))

* Prettier seek arrows on playback screen. ([`020bffb`](https://github.com/mps-youtube/yewtube/commit/020bffbe40e1781473669eea3d545f531165b063))

* Reduce delay on ctrl-c to exit playlist playback

Trim long ls info message ([`3be73b5`](https://github.com/mps-youtube/yewtube/commit/3be73b57f2bfc938f7267de7971928d49df781f7))

* v0.18.31 ([`5e8bfb4`](https://github.com/mps-youtube/yewtube/commit/5e8bfb41b80843c564a2a43b4c339accf3895570))

* cache top period requests ([`4747c6a`](https://github.com/mps-youtube/yewtube/commit/4747c6acf93d052d2c66fb9cc2ec021147de6295))

* Tidy http memoization code ([`0a2ec9b`](https://github.com/mps-youtube/yewtube/commit/0a2ec9b0a31aeecc12211c217687ec73eaaffce8))

* added HTTP request memoization ([`cdf5e24`](https://github.com/mps-youtube/yewtube/commit/cdf5e2454e72415b1376348e8d57059daa91de05))

* 0.18.30 ([`e711974`](https://github.com/mps-youtube/yewtube/commit/e711974c3754b7f335c58378df64ae8248cd9b90))

* added next/prev results option ([`66e67bf`](https://github.com/mps-youtube/yewtube/commit/66e67bf33b2ff3d83cbe2983a203b4366e019b82))

* Documented next/prev page ([`5df9b8a`](https://github.com/mps-youtube/yewtube/commit/5df9b8aef1ae6faf5a0056d91950f980dd26ece4))

* version 0.18.29 ([`7c71ad0`](https://github.com/mps-youtube/yewtube/commit/7c71ad0f77830c7bf0fce525751c47cbfe65b230))

* Error handling for unavailable tracks ([`a0a9699`](https://github.com/mps-youtube/yewtube/commit/a0a969920932d4947ba66d93139ae1dce5ab210f))

* Fix top tracks request regex ([`36f73b6`](https://github.com/mps-youtube/yewtube/commit/36f73b6077d44726b6c4be2ce09265fabc305cbe))

* 0.18.28 ([`9ceb247`](https://github.com/mps-youtube/yewtube/commit/9ceb247ffa4747ce0673503ce7812365f2fcdf90))

* Fix bad top tracks regex ([`9391a60`](https://github.com/mps-youtube/yewtube/commit/9391a6096229ca867293eb30504a9983cc9ae6b3))

* Simplify OS X notes ([`23a5a1e`](https://github.com/mps-youtube/yewtube/commit/23a5a1e70aad396a29b5595b1251abe331c35d98))

* Add checkupdate option ([`d2e03fe`](https://github.com/mps-youtube/yewtube/commit/d2e03fe911618fe159093ff73c6f882427d8ec0f))

* 0.18.27 ([`f3c84b0`](https://github.com/mps-youtube/yewtube/commit/f3c84b02678b34ac9b1b5a34c7657b78ea8944fd))

* 0.18.27 ([`3324ce4`](https://github.com/mps-youtube/yewtube/commit/3324ce4636e6227c7b6344f5ea34e1a20c6c07ab))

* Add version ([`d156058`](https://github.com/mps-youtube/yewtube/commit/d1560586f6e5fb8d4244b83c5bd340bb9bb24d1f))

* Add &#34;restart required&#34; message when toggling COLOURS&#34; ([`1c88c1b`](https://github.com/mps-youtube/yewtube/commit/1c88c1b63aae89cca8ea68b8a4657c479c5d061d))

* fix colours not being set ([`6a5fdfd`](https://github.com/mps-youtube/yewtube/commit/6a5fdfd390a9c401ecf46d983e531e4e735f6bc9))

* 0.18.26 ([`242b834`](https://github.com/mps-youtube/yewtube/commit/242b834a684f97ce62f5a55e9f8bfd2caacdacda))

* Add options to modify config ([`f7f6a19`](https://github.com/mps-youtube/yewtube/commit/f7f6a19b2ddb616181b9f617fdacfef73664da52))

* v0.18.25 ([`2840138`](https://github.com/mps-youtube/yewtube/commit/284013828b8c73e984368014152da45d9de3abb9))

* Add configuration options ([`d26f29e`](https://github.com/mps-youtube/yewtube/commit/d26f29e4d5efa212bfee00d12b563b75651fb5c6))

* Help for changing config ([`a184401`](https://github.com/mps-youtube/yewtube/commit/a18440117391846584d1464624068563a8e40b0c))

* v0.18.24 ([`fb212c6`](https://github.com/mps-youtube/yewtube/commit/fb212c67b59eddd0bc8c7082ca65ec6a13fdbfb4))

* Tidier help ([`125afa0`](https://github.com/mps-youtube/yewtube/commit/125afa08be94697a2a00a00dcfb34e88e60280d1))

* Neater encapsulation ([`d02682b`](https://github.com/mps-youtube/yewtube/commit/d02682b2d91025f97abb0a0b214ef67d762c781a))

* Update help for open and view commands. ([`15dd22e`](https://github.com/mps-youtube/yewtube/commit/15dd22eea5ba45f80eb2fb02c8049e0f0efe06c8))

* Allow ID number in open &amp; view commands ([`07f1c86`](https://github.com/mps-youtube/yewtube/commit/07f1c862c3371840bc707360140ba0d07bb500a1))

* fix missing comma ([`7499551`](https://github.com/mps-youtube/yewtube/commit/7499551b66348147ba34de78532cb1447e93bd54))

* 0.18.23 ([`e1c28a9`](https://github.com/mps-youtube/yewtube/commit/e1c28a92f79ee1c999e5fa6f5d4338ed01c3a149))

* Use unicode regexp&#39;s ([`30f9471`](https://github.com/mps-youtube/yewtube/commit/30f947147b831d283763773ee23f771bc474ac1a))

* catch case when content-length is none ([`361dfe3`](https://github.com/mps-youtube/yewtube/commit/361dfe35ea1acddd9685afbcb637454e6d28f279))

* Print on same line when showing help ([`ff29164`](https://github.com/mps-youtube/yewtube/commit/ff291647e221d83e4df3effd1f40ac7e7da0e475))

* v0.18.22 ([`8685614`](https://github.com/mps-youtube/yewtube/commit/8685614391c7469ea18dc62bc77af67e5cfda18a))

* new: mv to rename playlists

rmp to remove playlist by ID ([`7b845e5`](https://github.com/mps-youtube/yewtube/commit/7b845e5442799a9027f1470e5b2464135db90667))

* Documented new commands ([`47927aa`](https://github.com/mps-youtube/yewtube/commit/47927aa366c71fd18d9156c34d78a7f150fb148b))

* add `+best` and `+good` options ([`c8a92b4`](https://github.com/mps-youtube/yewtube/commit/c8a92b4926b8ebc1b38fd4fe5821bad203f77076))

* version 0.18.21 ([`341716b`](https://github.com/mps-youtube/yewtube/commit/341716b50593593bda315f53711234905683c37b))

* Add notes for +best and +good ([`26e0308`](https://github.com/mps-youtube/yewtube/commit/26e0308abb12f4acaa25e48068fac239124ae43a))

* 0.18.20 ([`35a48e3`](https://github.com/mps-youtube/yewtube/commit/35a48e3a5db0e543c1e82f9578e0d937af25fad4))

* Catch EOFError on ctrl-c exit ([`ca8e3c7`](https://github.com/mps-youtube/yewtube/commit/ca8e3c789e8e877ba9e4b2d7f7e0b8c779d3fcc1))

* Use dict comprehension, remove pylint comments ([`40c914d`](https://github.com/mps-youtube/yewtube/commit/40c914d9706a340ba24a0d01953959474a64aba0))

* minor corrections ([`8af0758`](https://github.com/mps-youtube/yewtube/commit/8af0758f4a5c670d89fb95fa17a8b36c65453815))

* Specify ranges with N- and -N.  Commas or spaces

Better user input handling /branching
more concise functions ([`8b566b2`](https://github.com/mps-youtube/yewtube/commit/8b566b2cad0222a8379233fa10cb02ba0827de84))

* Documented updated usage ([`7b23874`](https://github.com/mps-youtube/yewtube/commit/7b238742af5ec467af49edf6c75a7600eeb40ceb))

* Version 0.18.19 ([`458dc1f`](https://github.com/mps-youtube/yewtube/commit/458dc1f815b7fdd2d026ab3ba6a700ce318ceeaf))

* debugging mode based on file ([`2265ed8`](https://github.com/mps-youtube/yewtube/commit/2265ed800d0c1c76775f7ef07d8237b0efdf684f))

* fix for &#39;track no longer available&#39; message ([`afede90`](https://github.com/mps-youtube/yewtube/commit/afede90247c95a959e8e4ac3e871efaf9da4a372))

* Version 0.8.18 ([`c6c365f`](https://github.com/mps-youtube/yewtube/commit/c6c365fe9b6dd7966d967f577a2c5a83babac2d6))

* added for pypi ([`e4c9791`](https://github.com/mps-youtube/yewtube/commit/e4c9791aa2af05573917501f7c8399938df76fa1))

* bump version number ([`db21679`](https://github.com/mps-youtube/yewtube/commit/db216798cc50588f5322164e57eeecb4ca82b7da))

* bump version number ([`146b301`](https://github.com/mps-youtube/yewtube/commit/146b30158149816a7f49b8ca2de48d116836eec7))

* bump version number ([`b599798`](https://github.com/mps-youtube/yewtube/commit/b5997987989919a1946a09505a57a9fa4d59fd59))

* Better error / help messages for invalid playlist names ([`fff8b87`](https://github.com/mps-youtube/yewtube/commit/fff8b87022df0c2d1959a52a33ee1c22491e78ae))

* Version 0.18.15 ([`89ebbb3`](https://github.com/mps-youtube/yewtube/commit/89ebbb303ee71bcf60b33d6b063e6b97f899bdbe))

* Added new &#34;view&#34; command ([`163d95e`](https://github.com/mps-youtube/yewtube/commit/163d95ed537aa77bde1925cea0ae234953ba8c1d))

* Documented new &#34;view&#34; command ([`6938e63`](https://github.com/mps-youtube/yewtube/commit/6938e63ed42d8005486e5c413e011af9c2b81cef))

* Change version number ([`727c9b4`](https://github.com/mps-youtube/yewtube/commit/727c9b4c59a6ee82cab8137dd9a600bd925523d1))

* Change version number ([`556c727`](https://github.com/mps-youtube/yewtube/commit/556c727de18121fe8c84496cfe9eda5ba939550b))

* deleted blank line at end of file ([`0af54c6`](https://github.com/mps-youtube/yewtube/commit/0af54c616a0e31580b96dda2608243177ab6fff2))

* catch socket timeout ([`1de0c17`](https://github.com/mps-youtube/yewtube/commit/1de0c17b51c3744f1a59cb190140d43e69776903))

* test-ignore ([`16f2f2b`](https://github.com/mps-youtube/yewtube/commit/16f2f2bba08615720132b9dacd38fba5055a6eb1))

* test-ignore ([`9c36151`](https://github.com/mps-youtube/yewtube/commit/9c36151e031768f32c6d876c612ffbb661b65332))

* Moved string to strings dict ([`fa2757e`](https://github.com/mps-youtube/yewtube/commit/fa2757ecf13a67e8b4704e8ed79a777b75f1d2e6))

* Modified links to display correctly on pypi ([`0024aa0`](https://github.com/mps-youtube/yewtube/commit/0024aa0fbaa23d863b8c56db7f5746b9f2e5a66f))

* Use README.rst for long_description ([`8837d18`](https://github.com/mps-youtube/yewtube/commit/8837d186d7a33c7605caf032a1dd4887a5c5358f))

* changed README from md to rst ([`9f4c25b`](https://github.com/mps-youtube/yewtube/commit/9f4c25bb4fb9edf096bf3fa696bde7548970710f))

* added ignore files ([`c570e45`](https://github.com/mps-youtube/yewtube/commit/c570e45ce6774d98782399ae42dd342758390c4f))

* correction ([`f246a76`](https://github.com/mps-youtube/yewtube/commit/f246a768935ed4a8082a0dfc7d4075da93265a55))

* Changed error displayed for HTTPError ([`c28362c`](https://github.com/mps-youtube/yewtube/commit/c28362c204b61c0d18a5fc1b29236aa2b14fd740))

* Version 0.8.13 ([`aa420ce`](https://github.com/mps-youtube/yewtube/commit/aa420cee59b173aa8a2c954cf592928523296b06))

* add fix for glib get_special_user_dirs returns None ([`070b00c`](https://github.com/mps-youtube/yewtube/commit/070b00cd2a3c56abbba83c2fb5da6d7538b867b8))

* show logo during search ([`c52cb6d`](https://github.com/mps-youtube/yewtube/commit/c52cb6d9d1fc3e7c4b5caf9f65ecce148e6ec619))

* Consolidated strings ([`1295e37`](https://github.com/mps-youtube/yewtube/commit/1295e37aa794b75505671bed5f4dd9fd5350331c))

* version 0.18.11 ([`c1b2a7b`](https://github.com/mps-youtube/yewtube/commit/c1b2a7bc2f9c2ade4dcac84b3f6803824ad4c9bf))

* Added logo, formatted help ([`eb2713f`](https://github.com/mps-youtube/yewtube/commit/eb2713fcc8810e4004ff5ff60b4c0989438551fa))

* version 0.18.10 ([`130034a`](https://github.com/mps-youtube/yewtube/commit/130034af5f2fbbdd6f58e2800ca874135f3b3be3))

* catch glib attribute error ([`f2f001a`](https://github.com/mps-youtube/yewtube/commit/f2f001ab01466ff05738d7a350714eec01a75e47))

* version number ([`9dd6501`](https://github.com/mps-youtube/yewtube/commit/9dd6501d75df849336f19c68089b2742f93d7600))

* corrections ([`bef1852`](https://github.com/mps-youtube/yewtube/commit/bef18527be22200082a4e661636a46e0f92aefab))

* correction ([`79212d5`](https://github.com/mps-youtube/yewtube/commit/79212d5fb148cc8e4a380a4962f55f25c2aefe3f))

* Add songs to saved playlist ([`0b3ba32`](https://github.com/mps-youtube/yewtube/commit/0b3ba3232e23469260a3b55c0f06207d9400bdeb))

* bump version number ([`38616d2`](https://github.com/mps-youtube/yewtube/commit/38616d25203c42dc37aabf40dc67cfed960fd172))

* Added notes on adding to saved playlist ([`6e15ecc`](https://github.com/mps-youtube/yewtube/commit/6e15ecc027d2d039ad7b0e1925bfd9e325d39e69))

* code deduplication ([`16511fe`](https://github.com/mps-youtube/yewtube/commit/16511fe86f2142b9dd6271842e50043ee3a39e33))

* Fix content not displaying after playback in repeat mode ([`cc93a83`](https://github.com/mps-youtube/yewtube/commit/cc93a83ff7d426f2564ef13d48d2439c2b3b78d2))

* Add shuffle and repeat feature ([`adfc467`](https://github.com/mps-youtube/yewtube/commit/adfc4677d7adfde46949bd7b64476f9175503130))

* Add notes on shuffle and repeat ([`17a94d8`](https://github.com/mps-youtube/yewtube/commit/17a94d83851a60699e2437dc57df8c9f56d19b71))

* bump version number ([`46fad1c`](https://github.com/mps-youtube/yewtube/commit/46fad1c6c5b8bc23cc4bfcd722216858f7b75321))

* fix errors ([`66cc43c`](https://github.com/mps-youtube/yewtube/commit/66cc43c0af6d2553a5bb3f2de3d661fe8e1f01fa))

* bump version number ([`c9be10b`](https://github.com/mps-youtube/yewtube/commit/c9be10b4161ad699c734295428d5b5ba42c87b2f))

* Fix bugs, neater playlist listing ([`00bb6ea`](https://github.com/mps-youtube/yewtube/commit/00bb6ea0e127ba9fca98efd5240b677e844519ed))

* Change lp command to ls ([`b983901`](https://github.com/mps-youtube/yewtube/commit/b98390130c0dc860c69666c974661c132f5b8a39))

* bump version number ([`4dc6574`](https://github.com/mps-youtube/yewtube/commit/4dc657425ba3b936f8a88b052633c96fdab6363b))

* bug fixes ([`69c2282`](https://github.com/mps-youtube/yewtube/commit/69c2282896f3144ac40d0ef4eaec09050b008732))

* Updated README.me ([`e2da4bf`](https://github.com/mps-youtube/yewtube/commit/e2da4bf58735dd688b9abc0777cea0ecfc461ae2))

* Bump version number ([`30128ca`](https://github.com/mps-youtube/yewtube/commit/30128ca98b1cb0227f5fee2aa3e43b4666370a70))

* Prefix searches with . ([`8e17340`](https://github.com/mps-youtube/yewtube/commit/8e17340e685319b67ad736df5f1d3113278e3dad))

* Updated usage notes ([`571a170`](https://github.com/mps-youtube/yewtube/commit/571a17098ad8b8d9c9b6f7379ad586298c1d8ec1))

* bump version ([`7e30977`](https://github.com/mps-youtube/yewtube/commit/7e30977d1d81095762da766b484bb8a39cf13421))

* Correct problem with playlist access conflicting with model ([`fdc41e5`](https://github.com/mps-youtube/yewtube/commit/fdc41e546e40c67b65f19531613144fef01ae510))

* add rm all help ([`8b5dff2`](https://github.com/mps-youtube/yewtube/commit/8b5dff2eca4de309626c565d89d7b095b5c0a3a0))

* fix open playlist help message ([`aed07ed`](https://github.com/mps-youtube/yewtube/commit/aed07ed1394292a57502d2a1781a4fadc2e1d3ac))

* bump version ([`ebc1237`](https://github.com/mps-youtube/yewtube/commit/ebc1237eaeacc8a9a6b62bd51fe2a8c7fbaba938))

* fix line wrap ([`04776d3`](https://github.com/mps-youtube/yewtube/commit/04776d3049898c34de843e1267f04943743ae87f))

* bump version number ([`590e898`](https://github.com/mps-youtube/yewtube/commit/590e898a845f8eabcd2d76f968959444896b9137))

* save/load playlists to disk, edit playlists ([`b73f5cf`](https://github.com/mps-youtube/yewtube/commit/b73f5cf4813330d719094df2b6ebf3424a51924d))

* Added playlist instructions for save/load/edit ([`88b36fa`](https://github.com/mps-youtube/yewtube/commit/88b36faa9f5e8a8482749cf8203950cfb8913910))

* Merge branch &#39;master&#39; of https://github.com/np1/pms ([`a39ceeb`](https://github.com/mps-youtube/yewtube/commit/a39ceebfd46daa060feda52a19fd2d46c35b5b1f))

* Update pms

catch Glib.get_user_special_dir() returns None ([`3f43c0d`](https://github.com/mps-youtube/yewtube/commit/3f43c0d27d210716657bde2b4d1765d116aa1cf3))

* Catch AttributeError ([`0d63dce`](https://github.com/mps-youtube/yewtube/commit/0d63dce16087a58365c0985e35c1147b3a594036))

* playlists ([`a5e7ef9`](https://github.com/mps-youtube/yewtube/commit/a5e7ef95d4b7ca1aa470f38c5c6ba92dbda53720))

* Version 0.17 ([`cc218e1`](https://github.com/mps-youtube/yewtube/commit/cc218e18f0292ebc6681ec50cc477f5a3b56f7bc))

* Playlist creation and manipulation

add, delete, switch and move items in playlist
added help for above features ([`e91c0c3`](https://github.com/mps-youtube/yewtube/commit/e91c0c3fffb967cbbfecbe3cffc2fd9a5f3d050b))

* fix incorrectly placed blank ([`c2e4cef`](https://github.com/mps-youtube/yewtube/commit/c2e4cef0940a1a7b7acb463f6b92574285b53a11))

* Conditional utf8 decode of download directory path string
https://github.com/np1/pms/issues/20 ([`12681ce`](https://github.com/mps-youtube/yewtube/commit/12681cee1727c8d4e02ce7530a99d9813993c4e3))

* bump version number ([`237ec15`](https://github.com/mps-youtube/yewtube/commit/237ec1522124ef5d99baec2df46177fba953b5c9))

* pylint, pep8, pep257, mccabe, pyflakes ([`f8a530d`](https://github.com/mps-youtube/yewtube/commit/f8a530d6451b4a5b8d12d7e41b9db40d677ad762))

* catch KeyboardInterrupt on help screen ([`c41f4df`](https://github.com/mps-youtube/yewtube/commit/c41f4df0e9b55ebe82a17bec71dd60b571ed840b))

* tidier output for single track playback ([`321525d`](https://github.com/mps-youtube/yewtube/commit/321525dd789a1b4ccd1f6c7257e96a66dfbd512c))

* fix misplaced display attributes ([`4c0bc44`](https://github.com/mps-youtube/yewtube/commit/4c0bc44cdde20a6634856cdd45d4cc3a5cd12d76))

* Context-sensetive help ([`fb41798`](https://github.com/mps-youtube/yewtube/commit/fb41798b544635cc3988623bc458cc5a4b6c2e03))

* add utf8 decode for download directory ([`7996fa1`](https://github.com/mps-youtube/yewtube/commit/7996fa1586a2d2ed7265c7ed4c17144e41e2d330))

* bump version ([`7d363a3`](https://github.com/mps-youtube/yewtube/commit/7d363a3909361fc7df7dbb8f7a8e83f6b8fc32e5))

* gi.repository ([`46e2d01`](https://github.com/mps-youtube/yewtube/commit/46e2d015c5e5aa38b0c1b296b248ffb755569679))

* fix international download folder name with glib ([`7cd25a3`](https://github.com/mps-youtube/yewtube/commit/7cd25a3caa7c274a077154fb6b1e39048b5bf1ab))

* fix incorrect bitrate display ([`3accb73`](https://github.com/mps-youtube/yewtube/commit/3accb739220f5616119601a538c9cf76cece4679))

* bump version ([`33a4a4d`](https://github.com/mps-youtube/yewtube/commit/33a4a4dadcfc5e7dd464479ef98b250bd3ae3748))

* add seek UP, DOWN shortcut to playback dialog ([`ff09aa1`](https://github.com/mps-youtube/yewtube/commit/ff09aa1797ed57cc435cf6cf712630efde999e34))

* user interface improvements ([`ed57507`](https://github.com/mps-youtube/yewtube/commit/ed57507591add52da2155fbe774c77cb8a42ccad))

* bump version number ([`88988d5`](https://github.com/mps-youtube/yewtube/commit/88988d54f977b3496adb93e9c5d0818f458ae3d7))

* user interface improvements
better http/url error handling ([`b2191ea`](https://github.com/mps-youtube/yewtube/commit/b2191ea51c61967882a87a4a498a27ee97522d6a))

* bump version number ([`3686e7a`](https://github.com/mps-youtube/yewtube/commit/3686e7af5ac4b7deaa3e0f2ebb6c4f92fb910594))

* Further pimping of interface
Better urlopen error handling / timeouts ([`95c96e5`](https://github.com/mps-youtube/yewtube/commit/95c96e5a47a7189b31f3891f5a5ffe4f3ca6b003))

* bump version number ([`8ad6773`](https://github.com/mps-youtube/yewtube/commit/8ad6773a9b55b42a818b07c05b95637ed1de1b03))

* Better interface for multiple song playback dialog ([`9565c92`](https://github.com/mps-youtube/yewtube/commit/9565c92f71b08f3248bbddcb74bfa09131534ef7))

* bump version number ([`2a7ec05`](https://github.com/mps-youtube/yewtube/commit/2a7ec05b01d836f8aafbf5c01bce7e88ab1809b4))

* exit multiple playback with ctrl-c
add option to play all ([`f792a09`](https://github.com/mps-youtube/yewtube/commit/f792a0995d9036f58bd2e7c3c64b612132311896))

* exit multiple playback with ctrl-c
add option to play all ([`a7654ad`](https://github.com/mps-youtube/yewtube/commit/a7654ad53a64d0897cf77a253c5915a80847ed91))

* fix import error ([`cb76702`](https://github.com/mps-youtube/yewtube/commit/cb7670227dd2d9ac6d339d38813322e2569961a6))

* bump version number ([`88ed7bb`](https://github.com/mps-youtube/yewtube/commit/88ed7bbeaab416001dec54fac03f1708c98fd2a7))

* tidied birange function ([`5cc10e8`](https://github.com/mps-youtube/yewtube/commit/5cc10e84bd1fbad680bf3460601464dc690f0c7f))

* play a range of tracks from the search results ([`20e67f0`](https://github.com/mps-youtube/yewtube/commit/20e67f0a070cc6a7ade4a852d72559800b9450e3))

* get version number from pms ([`95e909b`](https://github.com/mps-youtube/yewtube/commit/95e909b6165a3e029121555dea3c43d4e09bcbfc))

* separate function for bitrate calculation
changed exit message, added link to home on github ([`1931884`](https://github.com/mps-youtube/yewtube/commit/1931884f232452723afef75014f601ebca2cd402))

* comments ([`604f3c0`](https://github.com/mps-youtube/yewtube/commit/604f3c0db057641f274d6465108992305b11459a))

* bump version number for pypi ([`05bb708`](https://github.com/mps-youtube/yewtube/commit/05bb7083acdbd32ac568bedb3cfe988e8c4b819f))

* better exception handling
better flow control
more blank lines for readability ([`0c9aa6d`](https://github.com/mps-youtube/yewtube/commit/0c9aa6d528e2349ea0b0a30d65e560ae34aff2ad))

* move get_top_period() function next to dosearch() ([`6918c1d`](https://github.com/mps-youtube/yewtube/commit/6918c1dc7cf98011787f1cbeeef318bcfe2db08e))

* bump version number ([`75ff5d2`](https://github.com/mps-youtube/yewtube/commit/75ff5d2f0b30a8f9f0b7111a6b03a907a02eedba))

* show average bitrate of VBR files ([`967c860`](https://github.com/mps-youtube/yewtube/commit/967c8601caa7d353a3bdd5d5d5f2899cd8881112))

* fix typo ([`4c6c229`](https://github.com/mps-youtube/yewtube/commit/4c6c2299a5fa1ab836cce912052252f64ba865a3))

* fix markdown ([`d147766`](https://github.com/mps-youtube/yewtube/commit/d14776686dd2e47f3125d59c11da0ce1843712b1))

* escape &lt;&gt; chars ([`ebfb59b`](https://github.com/mps-youtube/yewtube/commit/ebfb59beaa0640ac984de375e6f09258b915ab6f))

* updated usage example ([`f7d6b80`](https://github.com/mps-youtube/yewtube/commit/f7d6b80e39134126fe5bba47cdaafa163139a532))

* nicer formatting ([`852e7fc`](https://github.com/mps-youtube/yewtube/commit/852e7fca4c59024a684a33056d6c9ce1aca911a6))

* revert previous changes ([`6e2d340`](https://github.com/mps-youtube/yewtube/commit/6e2d3402d332ae53566ed4196cf413484489c7a7))

* fixed typo ([`eabe292`](https://github.com/mps-youtube/yewtube/commit/eabe292aa3bb432f0518e33c0f3ea078b904f79b))

* clear screen between searches ([`7fe5ee8`](https://github.com/mps-youtube/yewtube/commit/7fe5ee8fdc1ed91995059323f8fab4aaa6b90d76))

* added badges ([`0a9dd6f`](https://github.com/mps-youtube/yewtube/commit/0a9dd6f598217e0c2cc96a2a4a5c2944ded81d07))

* use README.md as long description ([`a805251`](https://github.com/mps-youtube/yewtube/commit/a805251a5ff2ff31f2f2456d8e8bcf2dce5c2a5b))

* fixed headings ([`4365a5c`](https://github.com/mps-youtube/yewtube/commit/4365a5c5862b9bde4b756dbb65ea6a14d339e45e))

* Updated to include upgrade notes
tidied formatting ([`b46fd86`](https://github.com/mps-youtube/yewtube/commit/b46fd86a40d24bc907cbc399b665419327d9d7dd))

* Display default mplayer keyboard shortcuts during playback ([`9176301`](https://github.com/mps-youtube/yewtube/commit/9176301756fd8abe60d52caf9fe8ceea2c3f7252))

* updated usage notes ([`7747542`](https://github.com/mps-youtube/yewtube/commit/774754263c488a4ef92ba7786da5691a843aad54))

* updated for interactive help ([`ac3e401`](https://github.com/mps-youtube/yewtube/commit/ac3e4016326d7def9b29b87e28ff9dac6916cb9f))

* Added help option ([`130bd7f`](https://github.com/mps-youtube/yewtube/commit/130bd7f84b7febc6cf32851fa5740bc5587e2017))

* Merge pull request #15 from viskor/patch-1

Update README.md ([`c11b28d`](https://github.com/mps-youtube/yewtube/commit/c11b28d25951ac4653f1b8ad99eb447f04d8cd8f))

* Update README.md ([`d6131ae`](https://github.com/mps-youtube/yewtube/commit/d6131ae261bf7a900f856af9f85dc0903bece61e))

* handle HTTPError ([`47b4aa4`](https://github.com/mps-youtube/yewtube/commit/47b4aa49c5ba258ea209d8ab8ef0bcecdc5afe83))

* partial url matching for playlist url ([`8b05d8b`](https://github.com/mps-youtube/yewtube/commit/8b05d8b9647a1124106621196cfb2d8d549714a0))

* Add feature to fetch playlist from website ([`b4a61b1`](https://github.com/mps-youtube/yewtube/commit/b4a61b1abfbd412a4703770bbb0b44755c4bcb66))

* utf8 encode for python &lt; 3 ([`f8a7e87`](https://github.com/mps-youtube/yewtube/commit/f8a7e8773041340ba03bc3e73e700f3b78fd80a3))

* added top music list for different periods ([`af866b0`](https://github.com/mps-youtube/yewtube/commit/af866b040f18b4787ea2a7c6ece9babbf5ab6d61))

* added some comments ([`2a8f49d`](https://github.com/mps-youtube/yewtube/commit/2a8f49d1ac3a2a64c590191d73d6808ea64e40a7))

* removed redundant conditionals. corrected some strings ([`4df41ae`](https://github.com/mps-youtube/yewtube/commit/4df41aed7ea7aaf42f5104331092fd5c4e05676b))

* Merge pull request #11 from WitzHsiao/master

add feature: display top musics list this week ([`dd173f9`](https://github.com/mps-youtube/yewtube/commit/dd173f9879715db303dad16085f8e5149b87c410))

* add feature: display top musics list this week ([`269eb98`](https://github.com/mps-youtube/yewtube/commit/269eb9885897005c6a637bf638c15c7170a74421))

* tidier import ([`055679c`](https://github.com/mps-youtube/yewtube/commit/055679c860803fb2814676940c2e180a9c2ded8f))

* removed ([`fad8372`](https://github.com/mps-youtube/yewtube/commit/fad8372fecdfce42a631867297a28e0417416470))

* added setup.py ([`86bdb01`](https://github.com/mps-youtube/yewtube/commit/86bdb01c53ca35429d4dbb783731c5328aded8b2))

* updated usage ([`2f4af06`](https://github.com/mps-youtube/yewtube/commit/2f4af0633df7eca5951f9ca4c270dfe6d34c4208))

* renamed pms.py to pms ([`3568bf9`](https://github.com/mps-youtube/yewtube/commit/3568bf9640af0cf48d184faa3e5c59cf1ea006be))

* corrected punctuation ([`e967619`](https://github.com/mps-youtube/yewtube/commit/e9676192bda769b31a3e1ec9279834f43a817e99))

* refactoring ([`7533421`](https://github.com/mps-youtube/yewtube/commit/7533421c794c8265dfa9a53c2435412cd30f0819))

* more housekeeping / code tidying ([`e58a14e`](https://github.com/mps-youtube/yewtube/commit/e58a14eb2ea32f78405647229364b5ac0d45b8cb))

* added comments, tidied some code ([`1fbd85c`](https://github.com/mps-youtube/yewtube/commit/1fbd85c12affa7ae66e66bfe8265c6ba406be6c0))

* undo previous fix to https://github.com/np1/pms/issues/6 as it breaks Python 3
compatibility in Linux ([`e128b91`](https://github.com/mps-youtube/yewtube/commit/e128b912e44c3ce278ff3cce7eecfc83869464ae))

* unicode fix for https://github.com/np1/pms/issues/6 ([`d8b4d3e`](https://github.com/mps-youtube/yewtube/commit/d8b4d3ed1ac58b6cbd2acd0706b754ca56c284fd))

* some minor changes ([`30c3a51`](https://github.com/mps-youtube/yewtube/commit/30c3a51c55f884271a1a6b526f296a17108dc5d4))

* Merge branch &#39;master&#39; of https://github.com/np1/pms ([`5eb3503`](https://github.com/mps-youtube/yewtube/commit/5eb350395afa875961275c0c202c9146888f7588))

* Merge pull request #5 from dukex/patch-1

Add information to MPlayerX on MacOSX ([`47d80b6`](https://github.com/mps-youtube/yewtube/commit/47d80b6449ab5ecc2440b6a7fb6ee8997c1a692f))

* Add information to MPlayerX on MacOSX

Added a note about MPlayerX ([`92a9fc4`](https://github.com/mps-youtube/yewtube/commit/92a9fc408c4d6be73e5b1fd086c94352d1ba7bfa))

* Merge pull request #2 from zyke/patch-1

Update README.md ([`d23bae4`](https://github.com/mps-youtube/yewtube/commit/d23bae4ac465817267844f80a67a45eea3d859ff))

* Update README.md

Updated README.md with instruction for mac osx 10.9. 
Need to install both X11 and mplayer, make link for mplayer. ([`08f5bda`](https://github.com/mps-youtube/yewtube/commit/08f5bda304df87842f41d5ab144c40b0d4300611))

* fixed unused import code check error ([`e34bb59`](https://github.com/mps-youtube/yewtube/commit/e34bb595f068bf3d125dac78a46ef4cae08a83fa))

* pyflakes, pep8 ([`8cfc38c`](https://github.com/mps-youtube/yewtube/commit/8cfc38cb527eeb31e64b66a059b08c5ef6ac4aa8))

* fix for windows (disable readline import) ([`34231ae`](https://github.com/mps-youtube/yewtube/commit/34231ae23ec82afb172f808d57b7d5eca2de49e6))

* Disable colours on Windows
Handle no mplayer installed ([`ebfe68b`](https://github.com/mps-youtube/yewtube/commit/ebfe68b2896fa81b2c9c519f59f59fe4f924e90f))

* added screenshot ([`0fb8783`](https://github.com/mps-youtube/yewtube/commit/0fb87835d21b025e04d2fd4f2908abde924239e3))

* added screenshot ([`02b1340`](https://github.com/mps-youtube/yewtube/commit/02b1340d60af1c3de7b7b16a46a4925e3628a6c7))

* readline import to fix cursor keys issue ([`f16e58b`](https://github.com/mps-youtube/yewtube/commit/f16e58bd90f242112084b5866d97c84fac8eaa30))

* Added pip install notes ([`40d7ca4`](https://github.com/mps-youtube/yewtube/commit/40d7ca42b7f852e278c82ec58275b365a845666c))

* Added -nolirc flag to suppress mplayer warning message ([`1e9ce81`](https://github.com/mps-youtube/yewtube/commit/1e9ce813a5c70de0a22602baad475517cfb330cb))

* Improved error handling ([`0a9a50b`](https://github.com/mps-youtube/yewtube/commit/0a9a50bfa45603d47eaf636b713ad3e70657ce80))

* updated features ([`535441d`](https://github.com/mps-youtube/yewtube/commit/535441ddb3866d31999a20ca76ccee4b3410557e))

* corrected download path ([`6b62b48`](https://github.com/mps-youtube/yewtube/commit/6b62b4889c692339ba18a31a5f8b808928cbc0fe))

* added usage example ([`4ab445e`](https://github.com/mps-youtube/yewtube/commit/4ab445ed81f64de1480e33463d362eaeada426ba))

* added DDIR (download dir) variable
used regexp&#39;s for input parsing
prettier column headings ([`e98447b`](https://github.com/mps-youtube/yewtube/commit/e98447b3a6ee02ea2ac34e23dd4ac931e4099269))

* Improved result table appearance ([`617b5c8`](https://github.com/mps-youtube/yewtube/commit/617b5c88968f03592e66b8754c85125409e9665f))

* . ([`34ae53d`](https://github.com/mps-youtube/yewtube/commit/34ae53dda3bcf4069811c6c4d6018e6a0b250596))

* removed logging feature
some tidying up ([`ec50612`](https://github.com/mps-youtube/yewtube/commit/ec5061203df562fa453d9cbf1f703cc4dc497e69))

* removed whitespace ([`096480b`](https://github.com/mps-youtube/yewtube/commit/096480b21e451d73f622449f7850dcf8a79679d0))

* Added license info ([`fb98ff3`](https://github.com/mps-youtube/yewtube/commit/fb98ff372bb29bbd6c1b360679a6de732ffb1a52))

* rewrite ([`d0de0af`](https://github.com/mps-youtube/yewtube/commit/d0de0afc8ff21deb75fe3621c4f0d76d776cc959))

* rewrite ([`fc6ca98`](https://github.com/mps-youtube/yewtube/commit/fc6ca9886fc3397060375cb2c2baa2d5c9c7bffc))

* Merge branch &#39;master&#39; of https://github.com/np1/pms ([`5a8baad`](https://github.com/mps-youtube/yewtube/commit/5a8baad9ed4bca30e1b442b8e26a5153e4c64db7))

* Update README.md ([`c227a7d`](https://github.com/mps-youtube/yewtube/commit/c227a7dc7c89541d219066e7dc4e6c8f14c3307e))

* removed redundant conditional ([`6a2dac0`](https://github.com/mps-youtube/yewtube/commit/6a2dac005f0feacd08e174eeaa98f02e233b1a07))

* removed logging ([`33aa5b9`](https://github.com/mps-youtube/yewtube/commit/33aa5b9a9416ca561e62c08b569d31c4e163fe60))

* added logging history ([`e36520c`](https://github.com/mps-youtube/yewtube/commit/e36520c15a4aef07ee306d4c648702d69157656f))

* added timeout ([`144c9a3`](https://github.com/mps-youtube/yewtube/commit/144c9a34d92e9b7406fb686a107e6f642d603f92))

* added requirement, mplayer ([`f8472cd`](https://github.com/mps-youtube/yewtube/commit/f8472cd13871981723c6973bfbde0747fd25754b))

* Update README.md

fixed formatting ([`bfa8f67`](https://github.com/mps-youtube/yewtube/commit/bfa8f672548a2d059c9c7c0f7a0427bc86c37130))

* added usage notes ([`e7f5ede`](https://github.com/mps-youtube/yewtube/commit/e7f5edeebbc9251d2b6eef21dcacd9619d8c848d))

* added file ([`e4fc1cc`](https://github.com/mps-youtube/yewtube/commit/e4fc1cc2b3b665e1e456a9896fc4cdadf11f9158))

* Initial commit ([`9de32be`](https://github.com/mps-youtube/yewtube/commit/9de32bec233fc5ac8170fd0c8375e9e9464d9435))
