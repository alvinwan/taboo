var launch_game_on_init = false;
var game;

var MAX_PASSES = 3;

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
  var Clock = function() {

    var time = 0;
    var clock;

    this.start = function() {
      clock = setInterval(tick, 1000);
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

    function tick() {
      time++;
      console.log(time);
    }
  }

  /**
   * Represents a round in the game. Handles immediate game actions i.e.,
   * correct, incorrect, or pass. This also handles the round timer, so it
   * processes pauses and resumes.
   */
  var Round = function(team) {

    var points = new Points();
    var passes = 0;
    var clock = new Clock();
    var card;

    this.start = function() {
      clock.start();
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
      if (this.passes < MAX_PASSES) {
        passes += 1;
        points.pass(team);
        next();
      } else {

      }
    }

    this.pause = function() {
      clock.pause();
    }

    this.resume = function() {
      clock.resume();
    }

    function next() {
      card = getNextCard();
      updateCardUI();
    }

    // TODO: actually get a new card
    function getNextCard() {
      data = words[Math.round(Math.random()*words.length)]
      return new Card(data[0], data[1])
    }

    function updateCardUI() {
      $('.keyword').html(card.word);
      for (var i = 0; i < card.unmentionables.length; i++) {
        $('.unmentionable-{0} .word'.format(i))
          .html(card.unmentionables[i]);
      }
    }
  }

  /**
   * General game interface, including utilities for launching the game
   * and generally maintaining the game's state. Processes round results and
   * updates game score.
   */
  var Game = function() {

    var currentTeam = 1;
    var points = new Points();
    var round;

    this.start = function() {
      currentTeam = 1;
      points = new Points();
      createRoundAndStart();
    }

    this.nextRound = function() {
      points.merge(this.round.points);
      currentTeam = getOtherTeam(this.currentTeam);
      createRoundAndStart(currentTeam);
    }

    this.getRound = function() {
      return round;
    }

    function createRoundAndStart(team) {
      round = new Round(team);
      round.start();
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
      this.tracker[team] += 1;
    }

    this.incorrect = function(team) {
      this.tracker[getOtherTeam(team)] += 1;
    }

    this.pass = function(team) {}

    this.merge = function(points) {
      for (var team in this.tracker) {
        this.tracker[team] += points[team];
      }
    }
  }

  /**
   * Compute ID of the other team, given the current team.
   */
  function getOtherTeam(team) {
    return 1 - team;
  }

  if (launch_game_on_init) {
    game = new Game();
    game.start();
  }
});
