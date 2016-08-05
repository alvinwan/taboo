var launch_game_on_init = false;
var game;

// http://stackoverflow.com/a/4673436/4855984
if (!String.prototype.format) {
  String.prototype.format = function() {
    var args = arguments;
    return this.replace(/{(\d+)}/g, function(match, number) {
      return typeof args[number] != 'undefined'
        ? args[number]
        : match
      ;
    });
  };
}

$(document).ready(function() {

  /**
   * Abstraction for configuration variables, which will store data in local
   * storage, to persist user settings, and handle the settings menu.
   */
  var Config = function() {
    this.team1_name = 'team1';
    this.team2_name = 'team2';
    this.max_passes = 3;
    this.round_duration_s = 3;
  }

  /**
   * Represents a card in the game.
   */
  var Card = function(word, unmentionables) {
    this.word = word;
    this.unmentionables = unmentionables;
  }

  /**
   * Abstraction for a clock
   */
  var Clock = function(config) {

    var time = 0;
    var clock;
    var onTickListener;

    this.start = function() {
      clock = setInterval(tick, 1000);
      updateTimeDisplay();
    }

    this.pause = function() {
      clearInterval(clock);
    }

    this.resume = function() {
      clock = setInterval(tick, 1000);
    }

    this.stop = function() {
      this.pause();
      time = 0;
    }

    this.setOnTickListener = function(listener) {
      onTickListener = listener;
    }

    function tick() {
      time++;
      updateTimeDisplay();
      onTickListener(time);
    }

    function updateTimeDisplay() {
      $('.time').html(config.round_duration_s-time);
    }
  }

  /**
   * Represents a round in the game. Handles immediate game actions i.e.,
   * correct, incorrect, or pass. This also handles the round timer, so it
   * processes pauses and resumes.
   */
  var Round = function(team, config) {

    var team = team;
    var points = new Points();
    var passes = 0;
    var clock = new Clock(config);
    var card;
    var onFinishListener;
    var onPauseListener;

    this.start = function() {
      clock.start();
      clock.setOnTickListener(function(time) {
        if (time >= config.round_duration_s) {
          finishRound();
        }
      });
      next();
    }

    this.correct = function() {
      points.correct(team);
      next();
    }

    this.incorrect = function() {
      points.incorrect(team);
      next();
    }

    this.pass = function() {
      if (passes < config.max_passes) {
        passes += 1;
        points.pass(team);
        next();
      } else {
        alert("You have used {0} of {1} passes.".format(
          passes,
          config.max_passes));
      }
    }

    this.pause = function() {
      clock.pause();
      if (onPauseListener) {
        onPauseListener();
      }
    }

    this.resume = function() {
      clock.resume();
    }

    this.setOnFinishListener = function(listener) {
      onFinishListener = listener;
    }

    this.setOnPauseListener = function(listener) {
      onPauseListener = listener;
    }

    this.getPoints = function() {
      return points;
    }

    function next() {
      card = getNextCard();
      updateCardUI();
    }

    function getNextCard() {
      data = words[Math.round(Math.random()*words.length)]
      return new Card(data[0], data[1])
    }

    function updateCardUI() {
      $('.game-element .keyword').html(card.word);
      for (var i = 0; i < card.unmentionables.length; i++) {
        $('.unmentionable-{0} .word'.format(i))
          .html(card.unmentionables[i]);
      }
    }

    function finishRound() {
      clock.stop();
      if (onFinishListener) {
        onFinishListener();
      }
    }
  }

  /**
   * General game interface, including utilities for launching the game
   * and generally maintaining the game's state. Processes round results and
   * updates game score.
   */
  var Game = function(config) {

    var currentTeam = 1;
    var points = new Points();
    var round;

    this.start = function() {
      currentTeam = 1;
      points = new Points();
      createRoundAndStart(currentTeam);
    }

    this.nextRound = function() {
      currentTeam = getOtherTeam(currentTeam);
      createRoundAndStart(currentTeam);
    }

    this.getRound = function() {
      return round;
    }

    function createRoundAndStart(team) {
      round = new Round(team, config);
      round.setOnFinishListener(function() {
        $('.intermission-action')
          .on('click', game.nextRound)
          .html('Team {0} Start'.format(currentTeam + 1));
        intermission();
      });
      round.setOnPauseListener(function() {
        $('.intermission-action')
          .on('click', round.resume)
          .html('Resume');
        intermission();
      })
      $('.intermission-element').each(function() {
        $(this).hide();
      });
      $('.game-element').each(function() {
        $(this).show();
      });
      round.start();
    }

    function intermission() {
      points.merge(round.getPoints());
      $('.intermission-element').each(function() {
        $(this).show();
      });
      $('.game-element').each(function() {
        $(this).hide();
      });

      $('.points-team1').html(points.get(0));
      $('.points-team2').html(points.get(1));
    }
  }

  /**
   * Abstraction for point deltas and tracking, handling point deductions and
   * rewards for each action.
   */
  var Points = function() {

    this.tracker = {0: 0, 1: 0};

    this.get = function(team) {
      return this.tracker[team];
    }

    this.correct = function(team) {
      this.tracker[team]++;
    }

    this.incorrect = function(team) {
      this.tracker[getOtherTeam(team)]++;
    }

    this.pass = function(team) {}

    this.merge = function(points) {
      for (var team in this.tracker) {
        this.tracker[team] += points.get(team);
      }
    }
  }

  /**
   * Compute ID of the other team, given the current team.
   */
  function getOtherTeam(team) {
    return 1 - team;
  }

  config = new Config();

  if (launch_game_on_init) {
    game = new Game(config);
    game.start();
  }
});
